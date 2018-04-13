#!/usr/bin/env pytohn
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

from lib.common import jsondate
from lib.common import lookup_key
from lib.common import detect_type

from lib.common import read_file
from lib.common import get_option

from lib.models import Hash
from lib.models import Host
from lib.models import User
from lib.models import Email
from lib.models import BitcoinAddress


help_dict = {
    'general': [
        'help', 'history', 'quit', 'cat apikeys', 'add apikey', 'banner'
    ],
    'artifacts': [
        'cat', 'rm', 'open', 'add source', 'add note'
    ],
    'modules': [
        'abusech', 'alienvault', 'blockchain', 'clearbit', 'censys', 'cymon',
        'dnsbrute', 'dnsresolve', 'geoip', 'fullcontact', 'gist', 'gitlab', 'github', 'hackedemails', 'hibp',
        'hunter', 'ipinfo', 'ipvoid', 'isc', 'keybase', 'mdl', 'nmap', 'passivetotal', 'pastebin', 'phishtank',
        'projecthp', 'reddit', 'rss', 'run', 'shodan', 'ssl', 'securitynews', 'threatcrowd',
        'threatexpert', 'totalhash', 'twitter', 'urlvoid', 'usersearch', 'virustotal', 'vxvault', 'web', 'whois'],
    'sessions': [
        'session', 'ls', 'clear'
    ]
}


class Console(cmd2.Cmd):
    def __init__(self):
        cmd2.Cmd.__init__(self,
            completekey='tab',
            persistent_history_file=get_option('core', 'hist_file', config),
            persistent_history_length=int(get_option('core', 'hist_size', config)))

        self.allow_cli_args = True
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


    def sigint_handler(self, signum, frame):
        pipe_proc = self.pipe_proc
        if pipe_proc is not None:
            pipe_proc.terminate()

        if self.session is not None:
            self.session.flush()

        raise KeyboardInterrupt('Caught keyboard interrupt; quitting ...')


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
        print('[ Modules ]')
        for cmd in help_dict['modules']:
            print(cmd)


    def do_artifacts(self, arg):
        """Show artifact specific commands"""
        print('[ Artifact Commands ]')
        for cmd in help_dict['artifacts']:
            print(cmd)


    def do_general(self, arg):
        """Show general commands"""
        print('[ General Commands ]')
        for cmd in help_dict['general']:
            print(cmd)


    def do_sessions(self, arg):
        """Show session commands"""
        print('[ Session Commands ]')
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


    def do_find(self, arg):
        """Search Mongo for artifact and display results

        Usage: find <artifact name>
               find <session id> """
        is_key, value = lookup_key(self.session, arg)

        if is_key and value is None:
            error('Unable to find artifact key in session (%s)' % arg)
            return
        elif is_key and value is not None:
            arg = value
        else:
            pass

        artifact_type = detect_type(arg)

        running('Searching for artifact (%s)' % arg)

        res = self.db.find(artifact_type, {'name': arg}, one=True)
        if res:
            print(json.dumps(res, indent=4, default=jsondate))


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
        _type = detect_type(arg)

        if _type == 'email':
            item = Email(email_address=arg)

        elif _type == 'host':
            item = Host(host=arg)

        elif _type == 'user':
            item = User(username=arg)

        elif _type == 'hash':
            item = Hash(hash=arg)

        elif _type == 'bitcoin':
            item = BitcoinAddress(addr=arg)

        else:
            warning('Must specify one of type: email, host, user, bitcoin')
            return

        if not self.db.exists(_type, {'name': arg}):
            _id = self.db.insert_one(_type, item)
            if _id is not None:
                success('Indexed new artifact for analysis. MongoDB ID (%s)' % _id)

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


    def do_delete(self, arg):
        """Remove artifact from database by name or ID

        Usage: delete <name> """
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
               cat <artifact name> """
        if arg == 'apikeys':
            data = json.load(open(api_keys, 'rb'))
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
            warning('Cannot find list file on disk (%s)' % arg)
            return

        artifacts = read_file(arg, True)
        for artifact in artifacts:
            a = None
            artifact_type = detect_type(artifact)

            if artifact_type == 'host':
                a = Host(host=artifact)

                if not self.db.exists(artifact_type, {'name': artifact}):
                    self.db.insert_one(artifact_type, a)

            elif artifact_type == 'email':
                a = Email(artifact)

                if not self.db.exists(artifact_type, {'name': artifact}):
                    self.db.insert_one(artifact_type, a)

            elif artifact_type == 'hash':
                a = Hash(artifact)

                if not self.db.exists(artifact_type, {'name': artifact}):
                    self.db.insert_one(artifact_type, a)

            elif artifact_type == 'btc':
                a = BitcoinAddress(artifact)

                if not self.db.exists(artifact_type, {'name': artifact}):
                    self.db.insert_one(artifact_type, a)

            elif artifact_type == 'user':
                a = User(artifact)

                if not self.db.exists(artifact_type, {'name': artifact}):
                    self.db.insert_one(artifact_type, a)

            else:
                info('Cannot determine type for artifact (%s)' % artifact)

            if a is not None:
                if self.session is not None:
                    _id = self.session.count_queued() + 1
                    self.session.set(_id, artifact)

        success('Finished loading artifact list')


    def do_report(self, arg):
        """Save artifact report as JSON file

        Usage: report <artifact name>
               report <session id> """
        _type = detect_type(arg)

        result = self.db.find(_type, {'name': arg}, one=True)
        if len(result) == 0:
            warning('No entry found for artifact (%s)' % arg)
        else:
            report = storage.JSON(result)
            report.save()
            if os.path.exists(report.file_path):
                success('Saved artifact report (%s)' % report.file_path)
            else:
                error('Failed to properly save report')


    def do_abusech(self, arg):
        """Search Abuse.ch for artifact details """
        pass


    def do_alienvault(self, arg):
        """Search AlienVault for artifact """
        pass


    def do_clearbit(self, arg):
        """Search Clearbit for email address """
        self.dispatch.submit(self.session, 'clearbit', arg)


    def do_censys(self, arg):
        """Search Censys for IPv4 address """
        self.dispatch.submit(self.session, 'censys', arg)


    def do_cymon(self, arg):
        """Search Cymon for host """
        self.dispatch.submit(self.session, 'cymon', arg)


    def do_dnsbrute(self, arg):
        """Enumerate DNS subdomains of FQDN """
        pass


    def do_dnsresolve(self, arg):
        """Retrieve DNS records for host """
        self.dispatch.submit(self.session, 'dnsresolve', arg)


    def do_geoip(self, arg):
        """Retrieve Geolocation details for host """
        self.dispatch.submit(self.session, 'geoip', arg)


    def do_fullcontact(self, arg):
        """Search FullContact for email address """
        pass


    def do_gist(self, arg):
        """Search Github Gist's for artifact as string """
        pass


    def do_gitlab(self, arg):
        """Check Gitlab for active username """
        pass


    def do_github(self, arg):
        """Check GitHub for active username"""
        self.dispatch.submit(self.session, 'github', arg)


    def do_hackedemails(self, arg):
        """Check hacked-emails.com for email address"""
        self.dispatch.submit(self.session, 'hackedemails', arg)


    def do_hibp(self, arg):
        """Check HaveIBeenPwned for email address"""
        self.dispatch.submit(self.session, 'hibp', arg)


    def do_ipinfo(self, arg):
        """Retrieve ipinfo resutls for host"""
        self.dispatch.submit(self.session, 'ipinfo', arg)


    def do_ipvoid(self, arg):
        """Search IPVoid for host"""
        self.dispatch.submit(self.session, 'ipvoid', arg)


    def do_isc(self, arg):
        """Search SANS ISC for host"""
        self.dispatch.submit(self.session, 'sans', arg)


    def do_keybase(self, arg):
        """Search Keybase for active username"""
        self.dispatch.submit(self.session, 'keybase', arg)


    def do_monitor(self, arg):
        """Setup active monitors for RSS Feeds, Pastebin, Gist, and other services"""
        pass


    def do_mdl(self, arg):
        """Search Malware Domain List for host"""
        pass


    def do_nmap(self, arg):
        """Run NMap discovery scan against host"""
        self.dispatch.submit(self.session, 'nmap', arg)


    def do_passivetotal(self, arg):
        """Search PassiveTotal for host"""
        self.dispatch.submit(self.session, 'passivetotal', arg)


    def do_pastebin(self, arg):
        """Search Pastebin for artifact as string"""
        pass


    def do_projecthp(self, arg):
        """Search Project Honeypot for host"""
        pass


    def do_reddit(self, arg):
        """Search Reddit for active username"""
        pass


    def do_rss(self, arg):
        """Read latest from RSS feed

        Usage: rss <feed url>"""


    def do_run(self, arg):
        """Run all modules for artifact type

        Usage: run <artifact name>"""

    def do_securitynews(self, arg):
        """Get current cybersecurity headlines from Google News"""
        self.dispatch.submit(self.session, 'securitynews', arg)


    def do_shodan(self, arg):
        """Query Shodan for host"""
        self.dispatch.submit(self.session, 'shodan', arg)


    def do_source(self, arg):
        """ Set the source for the most recent artifact added to a session """
        last = self.session.receive('artifacts')
        _type = detect_type(last)

        if self.db.exists(_type, {'name': last}):
            self.db.update_one(_type, {'name': last}, {'source': arg})
            success('Added source to artifact entry (%s: %s)' % (last, arg))
        else:
            warning('Failed to find last artifact in MongoDB. Run "new <artifact name>" before using the source command')


    def do_threatcrowd(self, arg):
        """Search ThreatCrowd for host"""
        pass


    def do_threatexpert(self, arg):
        """Search ThreatExper for host"""
        pass


    def do_totalhash(self, arg):
        """Search TotalHash for host"""
        pass


    def do_twitter(self, arg):
        """Get Twitter info for username"""
        pass


    def do_urlvoid(self, arg):
        """Search URLVoid for domain name"""
        self.dispatch.submit(self.session, 'urlvoid', arg)


    def do_usersearch(self, arg):
        """Search Usersearch.com for active usernames"""
        pass


    def do_virustotal(self, arg):
        """Search VirusTotal for IPv4, FQDN, or Hash"""
        self.dispatch.submit(self.session, 'virustotal', arg)


    def do_vxvault(self, arg):
        """Search VXVault for IPv4 or FQDN"""
        pass

    def do_web(self, arg):
        """Fingerprint webserver"""
        pass


    def do_whois(self, arg):
        """Perform WHOIS lookup on host"""
        self.dispatch.submit(self.session, 'whois', arg)


    def do_whoismind(self, arg):
        """Search Whois Mind for domains associated to an email address"""
        self.dispatch.submit(self.session, 'whoismind', arg)


if __name__ == '__main__':
    global config
    global api_keys
    global output_dir

    os.system('clear')
    print(asciiart.banners[3])

    parser = argparse.ArgumentParser(description='Omnibus - https://github.com/InQuest/omnibus', epilog='Your resource for all things OSINT')
    ob_group = parser.add_argument_group('cli options')

    ob_group.add_argument('-c', '--conf',
        help='path to config file',
        action='store',
        default='%s/etc/omnibus.conf' % os.path.dirname(os.path.realpath(__file__)),
        required=False)

    ob_group.add_argument('-k', '--keys',
        help='path to API keys file',
        action='store',
        default='%s/etc/apikeys.json' % os.path.dirname(os.path.realpath(__file__)),
        required=False)

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

    api_keys = args.keys

    if args.conf:
        if not os.path.exists(args.conf):
            error('Config file not found; exiting ...')
            sys.exit(1)

        info('Using configuration file (%s)' % args.conf)

        config = args.conf

        output = get_option('core', 'reports', config)
        debug = True if get_option('core', 'debug', config) == '1' else False

    else:
        output = args.output
        debug = args.debug

    if os.path.exists(output):
        if not os.path.isdir(output):
            error('Specified report output location is not a directory; exiting ...')
            sys.exit(1)
    else:
        info('Creating report output directory (%s) ...' % output)
        mkdir(output)

    console = Console()
    console.cmdloop()
