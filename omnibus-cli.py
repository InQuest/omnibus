#!/usr/bin/env python
##
# The OSINT Omnibus
# --
# InQuest, LLC. (2018)
# https://github.com/InQuest/omnibus
# https://www.inquest.net
# --
# Please see docs directory for license information.
##
import os
import sys
import cmd2
import json
import argparse

from lib import common
from lib import storage
from lib import asciiart

from lib.mongo import Mongo
from lib.cache import RedisCache
from lib.dispatch import Dispatch

from lib.common import info
from lib.common import mkdir
from lib.common import error
from lib.common import running
from lib.common import success
from lib.common import warning
from lib.common import bold_msg

from lib.common import pp_json
from lib.common import lookup_key
from lib.common import detect_type

from lib.common import read_file
from lib.common import get_option

from lib.models import create_artifact


help_dict = {
    'general': [
        'help', 'history', 'quit', 'cat', 'apikey', 'banner', 'set', 'clear', 'artifacts', 'general',
        'redirect', 'sessions', 'modules'
    ],
    'artifacts': [
        'new', 'cat', 'open', 'source', 'artifacts', 'delete'
    ],
    'modules': [
        'blockchain', 'clearbit', 'censys', 'csirtg', 'cymon',
        'dnsresolve', 'geoip', 'fullcontact', 'hackedemails', 'he', 'hibp',
        'ipinfo', 'ipvoid', 'isc', 'keybase', 'machine', 'nmap', 'passivetotal',
        'pgp', 'rss', 'shodan', 'threatcrowd',
        'threatexpert', 'twitter', 'urlvoid', 'virustotal', 'web', 'whois'],
    'sessions': [
        'session', 'ls', 'rm', 'wipe'
    ]
}


class Console(cmd2.Cmd):
    def __init__(self):
        cmd2.Cmd.__init__(self,
            completekey='tab',
            persistent_history_file=get_option('core', 'hist_file', config),
            persistent_history_length=int(get_option('core', 'hist_size', config)))

        self.allow_cli_args = False
        self.default_to_shell = False
        self.intro = 'Welcome to the Omnibus shell! Type "session" to get started or "help" to view all commands.'
        self.allow_redirection = True
        self.prompt = 'omnibus >> '
        self.redirector = '>'
        self.quit_on_sigint = False

        del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_eof
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_eos
        del cmd2.Cmd.do_load
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_pyscript
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_unalias
        del cmd2.Cmd.do__relative_load

        self.db = Mongo(config)
        self.dispatch = Dispatch(self.db)
        self.session = None

        if DEBUG:
            self.do_set('debug true')


    def sigint_handler(self, signum, frame):
        """Ensure Redis DB is cleared before exiting application"""
        pipe_proc = self.pipe_proc
        if pipe_proc is not None:
            pipe_proc.terminate()

        if self.session is not None:
            self.session.flush()

        raise KeyboardInterrupt('Caught keyboard interrupt; quitting ...')


    def default(self, arg):
        """Override default function for custom error message"""
        if arg.startswith('#'):
            return

        error('Unknown command')
        return


    def do_quit(self, _):
        """Exit Omnibus shell."""
        self._should_quit = True

        if self.session is not None:
            running('Clearing artifact cache ...')
            self.session.flush()

        warning('Closing Omnibus shell ...')
        return self._STOP_AND_EXIT


    def do_clear(self, arg):
        """Clear the console"""
        os.system('clear')


    def do_modules(self, arg):
        """Show module list"""
        bold_msg('[ Modules ]')
        for cmd in help_dict['modules']:
            print(cmd)


    def do_artifacts(self, arg):
        """Show artifact information and available commands"""
        bold_msg('[ Artifacts ]')
        for cmd in help_dict['artifacts']:
            print(cmd)


    def do_general(self, arg):
        """Show general commands"""
        bold_msg('[ General Commands ]')
        for cmd in help_dict['general']:
            print(cmd)


    def do_sessions(self, arg):
        """Show session commands"""
        bold_msg('[ Session Commands ]')
        for cmd in help_dict['sessions']:
            print(cmd)


    def do_redirect(self, arg):
        """ Show redirection command help """
        info('Omnibus supports command redirection to output files using the ">" character. For example, "cat host zeroharbor.org > zh.json" will pipe the output of the cat command to ./zh.json on disk.')


    def do_banner(self, arg):
        """Display random ascii art banner"""
        print(asciiart.show_banner())


    def do_session(self, arg):
        """Open a new session"""
        self.session = RedisCache(config)
        if self.session.db is None:
            error('Failed to connect to Redis back-end. Please ensure the Redis service is running')
        else:
            success('Opened new session')


    def do_ls(self, arg):
        """View current sessions artifacts"""
        if self.session is None:
            warning('No active session')
            return

        count = 0
        keys = self.session.db.scan_iter()
        for key in keys:
            value = self.session.get(key)
            print('[%s] %s' % (key, value))
            count += 1
        info('Active Artifacts: %d' % count)


    def do_wipe(self, arg):
        """Clear currently active artifacts """
        if self.session is not None:
            info('Clearing active artifacts from cache ...')
            self.session.flush()
            success('Artifact cache cleared')
        else:
            warning('No active session; start a new session by running the "session" command')


    def do_rm(self, arg):
        """Remove artifact from session by ID

        Usage: rm <session id>"""
        try:
            arg = int(arg)
        except:
            error('Artifact ID must be an integer')
            return

        if self.session is not None:
            if self.session.exists(arg):
                self.session.delete(arg)
                success('Removed artifact from cache (%s)' % arg)
            else:
                warning('Unable to find artifact by ID (%s)' % arg)
        else:
            warning('No active session; start a new session by running the "session" command')


    def do_new(self, arg):
        """Create a new artifact

        Artifacts are created by their name. An IP address artifacts name would be the IP address itself,
        an FQDN artifacts name is the domain name, and so on.

        Usage: new <artifact name> """
        artifact = create_artifact(arg)

        if not self.db.exists(artifact.type, {'name': artifact.name}):
            doc_id = self.db.insert_one(artifact.type, artifact)
            if doc_id is not None:
                success('Created new artifact (%s - %s)' % (artifact.name, artifact.type))

        if self.session is None:
            self.session = RedisCache(config)
            self.session.set(1, artifact.name)
            success('Opened new session')
            print('Artifact ID: 1')
        else:
            count = 0
            for key in self.session.db.scan_iter():
                count += 1
            _id = count + 1
            self.session.set(_id, artifact.name)
            print('Artifact ID: %s' % _id)


    def do_delete(self, arg):
        """Remove artifact from database by name or ID

        Usage: delete <name>
               delete <session id>"""
        is_key, value = lookup_key(self.session, arg)

        if is_key and value is None:
            error('Unable to find artifact key in session (%s)' % arg)
            return
        elif is_key and value is not None:
            arg = value
        else:
            pass

        artifact_type = detect_type(arg)
        self.db.delete_one(artifact_type, {'name': arg})


    def do_cat(self, arg):
        """View artifact details or list API keys

        Usage: cat apikeys
               cat <artifact name>"""
        if arg == 'apikeys':
            data = json.load(open(common.API_CONF, 'rb'))
            print json.dumps(data, indent=2)
        else:
            is_key, value = lookup_key(self.session, arg)

            if is_key and value is None:
                error('Unable to find artifact key in session (%s)' % arg)
                return
            elif is_key and value is not None:
                arg = value
            else:
                pass

            artifact_type = detect_type(arg)
            result = self.db.find(artifact_type, {'name': arg}, one=True)
            if len(result) == 0:
                info('No entry found for artifact (%s)' % arg)
            else:
                print json.dumps(result, indent=2, separators=(',', ':'))


    def do_open(self, arg):
        """Load text file list of artifacts

        Command will detect each line items artifact type, create the artifact,
        and add it to the current session if there is one.

        Usage: open <path/to/file.txt> """
        if not os.path.exists(arg):
            warning('Cannot find file on disk (%s)' % arg)
            return

        artifacts = read_file(arg, True)
        for artifact in artifacts:
            new_artifact = create_artifact(artifact)

            if not self.db.exists(new_artifact.type, {'name': new_artifact.name}):
                doc_id = self.db.insert_one(new_artifact.type, new_artifact)
                if doc_id is not None:
                    success('Created new artifact (%s - %s)' % (artifact.name, artifact.type))

            if self.session is None:
                self.session = RedisCache(config)
                self.session.set(1, arg)
                success('Opened new session')
                print('Artifact ID: 1')
            else:
                count = 0
                for key in self.session.db.scan_iter():
                    count += 1
                _id = count + 1
                self.session.set(_id, arg)
                print('Artifact ID: %s' % _id)

        success('Finished loading artifact list')


    def do_report(self, arg):
        """Save artifact report as JSON file

        Usage: report <artifact name>
               report <session id>"""
        is_key, value = lookup_key(self.session, arg)

        if is_key and value is None:
            error('Unable to find artifact key in session (%s)' % arg)
            return
        elif is_key and value is not None:
            arg = value
        else:
            pass

        _type = detect_type(arg)

        result = self.db.find(_type, {'name': arg}, one=True)
        if len(result) == 0:
            warning('No entry found for artifact (%s)' % arg)
        else:
            report = storage.JSON(data=result, file_path=output_dir)
            report.save()
            if os.path.exists(report.file_path):
                success('Saved artifact report (%s)' % report.file_path)
            else:
                error('Failed to properly save report')


    def do_machine(self, arg):
        """Run all modules available for an artifacts type

        Usage: machine <artifact name>
               machine <session id>"""
        result = self.dispatch.machine(self.session, arg)
        pp_json(result)


    # def do_abusech(self, arg):
    #    """Search Abuse.ch for artifact details """
    #    pass


    def do_blockchain(self, arg):
        """Search Blockchain.info for BTC address"""
        result = self.dispatch.submit(self.session, 'blockchain', arg)
        pp_json(result)


    def do_clearbit(self, arg):
        """Search Clearbit for email address """
        result = self.dispatch.submit(self.session, 'clearbit', arg)
        pp_json(result)


    def do_censys(self, arg):
        """Search Censys for IPv4 address """
        result = self.dispatch.submit(self.session, 'censys', arg)
        pp_json(result)


    def do_csirtg(self, arg):
        """Search CSIRTG for hash information"""
        result = self.dispatch.submit(self.session, 'csirtg', arg)
        pp_json(result)


    def do_cymon(self, arg):
        """Search Cymon for host """
        result = self.dispatch.submit(self.session, 'cymon', arg)
        pp_json(result)


    # def do_dnsbrute(self, arg):
    #     """Enumerate DNS subdomains of FQDN """
    #     pass


    def do_dnsresolve(self, arg):
        """Retrieve DNS records for host """
        result = self.dispatch.submit(self.session, 'dnsresolve', arg)
        pp_json(result)


    def do_geoip(self, arg):
        """Retrieve Geolocation details for host """
        result = self.dispatch.submit(self.session, 'geoip', arg)
        pp_json(result)


    def do_fullcontact(self, arg):
        """Search FullContact for email address """
        result = self.dispatch.submit(self.session, 'fullcontact', arg)
        pp_json(result)


    # def do_gist(self, arg):
    #     """Search Github Gist's for artifact as string """
    #     pass


    # def do_gitlab(self, arg):
    #     """Check Gitlab for active username """
    #     pass


    def do_github(self, arg):
        """Check GitHub for active username"""
        result = self.dispatch.submit(self.session, 'github', arg)
        pp_json(result)


    def do_hackedemails(self, arg):
        """Check hacked-emails.com for email address"""
        result = self.dispatch.submit(self.session, 'hackedemails', arg)
        pp_json(result)


    def do_he(self, arg):
        """Search Hurricane Electric for host"""
        result = self.dispatch.submit(self.session, 'he', arg)
        pp_json(result)


    def do_hibp(self, arg):
        """Check HaveIBeenPwned for email address"""
        result = self.dispatch.submit(self.session, 'hibp', arg)
        pp_json(result)


    def do_ipinfo(self, arg):
        """Retrieve ipinfo resutls for host"""
        result = self.dispatch.submit(self.session, 'ipinfo', arg)
        pp_json(result)


    def do_ipvoid(self, arg):
        """Search IPVoid for host"""
        result = self.dispatch.submit(self.session, 'ipvoid', arg)
        pp_json(result)


    def do_isc(self, arg):
        """Search SANS ISC for host"""
        result = self.dispatch.submit(self.session, 'sans', arg)
        pp_json(result)


    def do_keybase(self, arg):
        """Search Keybase for active username"""
        result = self.dispatch.submit(self.session, 'keybase', arg)
        pp_json(result)


    def do_monitor(self, arg):
        """Setup active monitors for RSS Feeds, Pastebin, Gist, and other services"""
        pass


    def do_mdl(self, arg):
        """Search Malware Domain List for host"""
        pass


    def do_nmap(self, arg):
        """Run NMap discovery scan against host"""
        result = self.dispatch.submit(self.session, 'nmap', arg)
        pp_json(result)


    def do_otx(self, arg):
        """Search AlienVault OTX for host or hash artifacts"""
        result = self.dispatch.submit(self.session, 'otx', arg)
        pp_json(result)


    def do_passivetotal(self, arg):
        """Search PassiveTotal for host"""
        result = self.dispatch.submit(self.session, 'passivetotal', arg)
        pp_json(result)


    def do_pastebin(self, arg):
        """Search Pastebin for artifact as string"""
        pass


    def do_pgp(self, arg):
        """Search PGP records for email address or user"""
        result = self.dispatch.submit(self.session, 'pgp', arg)
        pp_json(result)


    # def do_projecthp(self, arg):
    #     """Search Project Honeypot for host"""
    #    pass


    # def do_reddit(self, arg):
    #     """Search Reddit for active username"""
    #     pass


    def do_rss(self, arg):
        """Read latest from RSS feed

        Usage: rss <feed url>"""
        result = self.dispatch.submit(self.session, 'rss', arg, True)
        pp_json(result)


    # def do_securitynews(self, arg):
    #    """Get current cybersecurity headlines from Google News"""
    #    result = self.dispatch.submit(self.session, 'securitynews', arg, True)
    #    pp_json(result)


    def do_shodan(self, arg):
        """Query Shodan for host"""
        result = self.dispatch.submit(self.session, 'shodan', arg)
        pp_json(result)


    def do_source(self, arg):
        """Add source to given artifact or most recently added artifact if not specified

        Usage: source                            # adds to last created artifact
               source <artifact name|session id> # adds to specific artifact
        """
        if arg == '':
            last = self.session.receive('artifacts')
            _type = detect_type(last)
        else:
            _type = detect_type(arg)
            is_key, value = lookup_key(self.session, arg)

            if is_key and value is None:
                error('Unable to find artifact key in session (%s)' % arg)
                return
            elif is_key and value is not None:
                arg = value
            else:
                pass

        if self.db.exists(_type, {'name': last}):
            self.db.update_one(_type, {'name': last}, {'source': arg})
            success('Added source to artifact entry (%s: %s)' % (last, arg))
        else:
            warning('Failed to find last artifact in MongoDB. Run "new <artifact name>" before using the source command')


    def do_threatcrowd(self, arg):
        """Search ThreatCrowd for host"""
        result = self.dispatch.submit(self.session, 'threatcrowd', arg)
        pp_json(result)


    def do_threatexpert(self, arg):
        """Search ThreatExpert for host"""
        result = self.dispatch.submit(self.session, 'threatexpert', arg)
        pp_json(result)


    # def do_totalhash(self, arg):
    #     """Search TotalHash for host"""
    #     pass


    def do_twitter(self, arg):
        """Get Twitter info for username"""
        result = self.dispatch.submit(self.session, 'twitter', arg)
        pp_json(result)


    def do_urlvoid(self, arg):
        """Search URLVoid for domain name"""
        result = self.dispatch.submit(self.session, 'urlvoid', arg)
        pp_json(result)


    # def do_usersearch(self, arg):
    #     """Search Usersearch.com for active usernames"""
    #     pass


    def do_virustotal(self, arg):
        """Search VirusTotal for IPv4, FQDN, or Hash"""
        result = self.dispatch.submit(self.session, 'virustotal', arg)
        pp_json(result)


    def do_vxvault(self, arg):
        """Search VXVault for IPv4 or FQDN"""
        pass

    def do_web(self, arg):
        """Fingerprint webserver"""
        pass


    def do_whois(self, arg):
        """Perform WHOIS lookup on host"""
        result = self.dispatch.submit(self.session, 'whois', arg)
        pp_json(result)


    def do_whoismind(self, arg):
        """Search Whois Mind for domains associated to an email address"""
        result = self.dispatch.submit(self.session, 'whoismind', arg)
        pp_json(result)


if __name__ == '__main__':
    global config
    global api_keys
    global output_dir
    global DEBUG

    os.system('clear')
    print(asciiart.banners[1])

    parser = argparse.ArgumentParser(description='Omnibus - https://github.com/InQuest/omnibus')
    ob_group = parser.add_argument_group('cli options')

    ob_group.add_argument('-o', '--output',
        help='report output directory',
        action='store',
        default='%s/reports' % os.path.dirname(os.path.realpath(__file__)),
        required=False)

    ob_group.add_argument('-d', '--debug',
        help='enable full traceback on exceptions',
        action='store_true',
        default=False,
        required=False)

    args = parser.parse_args()

    config = '%s/etc/omnibus.conf' % os.path.dirname(os.path.realpath(__file__))

    output_dir = args.output
    DEBUG = args.debug

    info('Using configuration file (%s) ...' % config)
    info('Debug: %s' % DEBUG)

    if os.path.exists(output_dir):
        if not os.path.isdir(output_dir):
            error('Specified report output location is not a directory; exiting ...')
            sys.exit(1)
    else:
        info('Creating report output directory (%s) ...' % output_dir)
        mkdir(output_dir)

    console = Console()
    console.cmdloop()
