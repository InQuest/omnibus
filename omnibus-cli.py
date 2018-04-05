#!/usr/bin/env pytohn
##
# OSINT Omnibus
# main cli toolkit
# --
# https://www.deadbits.org - https://github.com/deadbits
##

import os
import cmd2
import sys
import json
import argparse

from lib import cache
from lib import mongo
from lib import storage
from lib import asciiart

from lib.common import is_ipv4
from lib.common import is_ipv6
from lib.common import is_fqdn
from lib.common import is_email
from lib.common import is_hash
from lib.common import is_btc_addr

from lib.common import info
from lib.common import mkdir
from lib.common import error
from lib.common import running
from lib.common import success
from lib.common import warning

from lib.common import read_file

from lib.models import Hash
from lib.models import Host
from lib.models import User
from lib.models import Email
from lib.models import BitcoinAddress


help_dict = {
    'general': [
        'help', 'history', 'quit', 'cat apikeys', 'add apikey'
    ],
    'artifacts': [
        'cat', 'rm', 'open', 'add source', 'add note'
    ],
    'modules': [
        'abusech', 'alienvault', 'blockchain', 'clearbit', 'censys', 'cymon',
        'dnsbrute', 'dnsresolve', 'geoip', 'fullcontact', 'gist', 'gitlab', 'github', 'hackedemails', 'hibp',
        'hunter', 'ipinfo', 'ipvoid', 'isc', 'keybase', 'mdl', 'nmap', 'passivetotal', 'pastebin', 'phishtank',
        'projecthp', 'reddit', 'rss', 'scribd', 'shodan', 'ssl', 'securitynews', 'threatcrowd',
        'threatexpert', 'totalhash', 'twitter', 'urlvoid', 'usersearch', 'virustotal', 'vxvault', 'web', 'whois'],
    'sessions': [
        'session', 'ls', 'clear'
    ]
}


class Console(cmd2.Cmd):
    def __init__(self):
        cmd2.Cmd.__init__(self,
            completekey='tab',
            persistent_history_file='~/.omnibus_hist',
            persistent_history_length=500)

        self.allow_cli_args = True
        self.allow_redirection = True
        self.prompt = 'omnibus >> '
        self.redirector = '>'
        self.nohelp = warning('Unknown command: "%s".')
        self.quit_on_sigint = False
        self.db = mongo.Mongo()
        self.session = None
        self.max_session_size = 100

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


    def check_type(self, _type):
        valid_types = ['host', 'user', 'email', 'hash']
        if _type in valid_types:
            return True
        return False


    def detect_type(self, arg):
        """ Determine type of given argument """
        if is_ipv4(arg):
            return 'host'
        elif is_fqdn(arg):
            return 'host'
        elif is_email(arg):
            return 'email'
        elif is_hash(arg):
            return 'hash'
        elif is_btc_addr(arg):
            return 'btc'
        else:
            return 'user'


    def get_cached_item_by_id(self, artifact_id):
        """ Return value of cached artifact by session ID """
        if self.session is None:
            return None

        if self.session.exists(int(artifact_id)):
            return self.session.get(int(artifact_id))
        return None

    def do_modules(self, arg):
        """Show module list"""
        for cmd in help_dict['modules']:
            print cmd

    def do_artifacts(self, arg):
        """Show artifact specific commands"""
        for cmd in help_dict['artifacts']:
            print cmd


    def do_general(self, arg):
        """Show general commands"""
        for cmd in help_dict['general']:
            print cmd


    def do_sessions(self, arg):
        """Show session commands"""
        for cmd in help_dict['sessions']:
            print cmd


    def do_redirect(self, arg):
        """ Show redirection command help """
        info('Omnibus supports command redirection to output files using the ">" character. For example, "cat host zeroharbor.org > zh.json" will pipe the output of the cat command to ./zh.json on disk.')


    def do_session(self, arg):
        """ Open a new session """
        self.session = cache.RedisCache()
        if self.session.db is None:
            error('Failed to connect to Redis back-end. Please ensure the Redis service is running')
        else:
            success('Opened new session')


    def do_ls(self, arg):
        """ View currently active artifacts """
        if self.session is None:
            warning('No active session')
            return

        info('Active Artifacts: %s' % self.session.count_queued)
        keys = self.session.db.scan_iter()
        for key in keys:
            value = self.session.get(key)
            print('[%s] %s' % (key, value))


    def do_find(self, arg):
        """ Find db-stored artifact by name and view results """
        info('Searching for artifact (%s)' % arg)

        if is_ipv4(arg) or is_ipv6(arg) or is_fqdn(arg):
            res = self.db.find('host', {'name': arg}, one=True)
        elif is_email(arg):
            res = self.db.find('email', {'name': arg}, one=True)
        elif is_hash(arg):
            res = self.db.find('hash', {'name': arg}, one=True)
        elif is_btc_addr(arg):
            res = self.db.find('btc', {'name': arg}, one=True)
        else:
            res = self.db.find('user', {'name': arg}, one=True)

        if res:
            print json.dumps(res, indent=2)


    def do_wipe(self, arg):
        """ Clear currently active artifacts """
        info('Clearing active artifacts from cache ...')
        self.session.clear_queued()
        success('Cache flushed succesfully')


    def do_rm(self, arg):
        """ Remove artifact from session by ID"""
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
        """ Create a new artifact: new <name> """
        _type = self.detect_type(arg)

        if _type == 'email':
            item = Email(email_address=arg)
        elif _type == 'host':
            item = Host(host=arg)
        elif _type == 'user':
            item = User(username=arg)
        elif _type == 'hash':
            item = Hash(hash=arg)
        else:
            warning('Must specify one of type: email, host, user, bitcoin')
            return

        if not self.db.exists(_type, {'name': arg}):
            _id = self.db.insert_one(_type, item)
            if _id is not None:
                success('Indexed new artifact for analysis. MongoDB ID (%s)' % _id)

        if self.session is None:
            self.session = cache.RedisCache()
            self.session.set(1, arg)
            success('Opened new session')
            print('Artifact ID: 1')
        else:
            _id = self.session.count_queued() + 1
            self.session.data[_id] = arg
            print('Artifact ID: %s' % _id)


    def do_delete(self, arg):
        """ Remove artifact from database by name: delete <name>"""
        _type = self.detect_type(arg)
        self.db.delete_one(_type, {'name': arg})


    def do_cat(self, arg):
        """ View artifact details by type and name or list API keys: cat apikeys | cat <artifact name> """
        if args == 'apikeys':
            data = json.load(open(conf, 'rb'))
            print json.dumps(data, indent=2)
        else:
            _type = self.detect_type(arg)
            result = self.db.find(_type, {'name': arg}, one=True)
            if len(result) == 0:
                info('No entry found for artifact (%s)' % arg)
            else:
                print json.dumps(result, indent=2, separators=(',', ':'))


    def do_open(self, arg):
        """ Load text file list of artifacts to be created: open <path/to/file.txt> """
        if not os.path.exists(arg):
            warning('Cannot find list file on disk (%s)' % arg)
            return

        artifacts = read_file(arg, True)
        for artifact in artifacts:
            if is_ipv4(artifact) or is_fqdn(artifact) or is_ipv6(artifact):
                a = Host(host=artifact)

                if not self.db.exists('host', {'name': artifact}):
                    self.db.insert_one('host', a)

            elif is_email(artifact):
                a = Email(artifact)

                if not self.db.exists('email', {'name': artifact}):
                    self.db.insert_one('email', a)

            elif is_hash(artifact):
                a = Hash(artifact)

                if not self.db.exists('hash', {'name': artifact}):
                    self.db.insert_one('hash', a)

            elif is_btc_addr(artifact):
                a = BitcoinAddress(artifact)

                if not self.db.exists('btc', {'name': artifact}):
                    self.db.insert_one('btc', a)

            else:
                info('Cannot determine type for artifact. Treating as username (%s)' % artifact)
                a = User(artifact)

                if not self.db.exists('user', {'name': artifact}):
                    self.db.insert_one('user', a)

            if self.session is not None:
                _id = self.session.count_queued() + 1
                self.session.set(_id, artifact)

        success('Finished loading artifact list')


    def do_report(self, arg):
        """ Save artifact report as JSON file: report <artifact name> """
        _type = self.check_type(arg)

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
        """ Search Abuse.ch for artifact details """
        pass


    def do_alienvault(self, arg):
        """ Search AlienVault for artifact """
        pass


    def do_clearbit(self, arg):
        """ Search Clearbit for email address """
        if is_email(arg):
            from lib.modules import clearbit

            result = clearbit.run(arg)
            if result:
                if self.db.exists('email', {'name': arg}):
                    self.db.update_one('email', {'name': arg}, {'data': {'clearbit': result}})
                    success('Saved Clearbit results:')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get Clearbit results (%s)' % arg)
        else:
            warning('Failed to get Clearbit results (%s)' % arg)


    def do_censys(self, arg):
        """ Search Censys for IPv4 address """
        from lib.modules import censys

        result = censys.run(arg)
        if result:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, {'data': {'censys': result}})
                success('Saved Censys.io results:')
            print json.dumps(result, indent=2)
        else:
            warning('Failed to get Censys IPv4 results (%s)' % arg)


    def do_cymon(self, arg):
        """ Search Cymon for host """
        pass


    def do_dnsbrute(self, arg):
        """ Enumerate DNS subdomains of FQDN """
        pass


    def do_dnsresolve(self, arg):
        """ Retrieve DNS records for host artifact """
        from lib.modules import dnsresolve

        result = dnsresolve.run(arg)

        if result:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, {'data': {'DNS': result}})
                success('Saved DNS resolution results:')
            print json.dumps(result, indent=2)
        else:
            warning('Failed to get DNS resolution results (%s)' % arg)


    def do_geoip(self, arg):
        """ Retrieve Geolocation details for host """
        from lib.modules import geoip

        result = geoip.run(arg)

        if result:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, {'data': {'geoip': result}})
                success('Saved geoIP results:')
            print json.dumps(result, indent=2)
        else:
            warning('Failed to get freegeoip results (%s)' % arg)


    def do_fullcontact(self, arg):
        """ Search FullContact for email address """
        pass


    def do_gist(self, arg):
        """ Search Github Gist's for artifact as string """
        pass


    def do_gitlab(self, arg):
        """ Check Gitlab for active username """
        pass


    def do_github(self, arg):
        """Check GitHub for active username"""
        from lib.modules import github

        result = github.run(arg)
        if result is not None:
            if self.db.exists('user', {'name': arg}):
                self.db.update_one('user', {'name': arg}, {'data': {'github': result}})
                success('Saved GitHub results:')
            print json.dumps(result, indent=2)
        else:
            warning('Failed to get GitHub results (%s)' % arg)


    def do_hackedemails(self, arg):
        """Check hacked-emails.com for email address"""
        from lib.modules import hackedemails

        if is_email(arg):
            result = hackedemails.run(arg)
            if result is not None:
                if self.db.exists('email', {'name': arg}):
                    self.db.update_one('email', {'name': arg}, {'data': {'hackedemails': result}})
                    success('Saved hacked-emails results:')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get hacked-emails results (%s)' % arg)
        else:
            error('Must specify email address')


    def do_hibp(self, arg):
        """Check HaveIBeenPwned for email address"""
        from lib.modules import hibp

        if is_email(arg):
            result = hibp.run(arg)
            if result is not None:
                if self.db.exists('email', {'name': arg}):
                    self.db.update_one('email', {'name': arg}, {'data': {'hibp': result}})
                    success('saved HIBP results to db.')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get HIBP results (%s)' % arg)
        else:
            error('Must specify email address')


    def do_ipinfo(self, arg):
        """Retrieve ipinfo resutls for host"""
        pass


    def do_ipvoid(self, arg):
        """Search IPVoid for host"""
        pass


    def do_isc(self, arg):
        """Search SANS ISC for host"""
        from lib.modules import sans

        if is_ipv4(arg) or is_fqdn(arg):
            result = sans.run(arg)
            if result is not None:
                if self.db.exists('host', {'name': arg}):
                    doc_id = self.db.update_one('host', {'name': arg}, {'data': {'isc': result}})
                    if doc_id is not None:
                        success('Saved SANS ISC results:')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get SANS ISC results (%s)' % arg)
        else:
            warning('Must specify IPv4 or FQDN artifact (%s)' % arg)


    def do_keybase(self, arg):
        """Search Keybase for active username"""
        from lib.modules import keybase

        result = keybase.run(arg)
        if result is not None:
            if self.db.exists('user', {'name': arg}):
                doc_id = self.db.update_one('user', {'name': arg}, {'data': {'keybase': result}})
                if doc_id is not None:
                    success('Saved Keybase results:')
            print json.dumps(result, indent=2)
        else:
            warning('Failed to get Keybase results (%s)' % arg)


    def do_monitor(self, arg):
        """Setup active monitors for RSS Feeds, Pastebin, Gist, and other services"""
        pass


    def do_mdl(self, arg):
        """Search Malware Domain List for host"""
        pass


    def do_nmap(self, arg):
        """Run NMap discovery scan against host"""
        running('starting NMap discovery scan ...')
        from lib.modules import nmap

        if is_ipv4(arg) or is_fqdn(arg):
            result = nmap.run(arg)
            if len(result['ports']) > 0:
                if self.db.exists('host', {'name': arg}):
                    self.db.update_one('host', {'name': arg}, {'data': {'nmap': result}})
                    success('Saved Nmap results:')
                for item in result['ports']:
                    print item
            else:
                warning('Nmap scan completed but no open ports found')
        else:
            error('Must specify a IPv4 or FQDN artifact')


    def do_passivetotal(self, arg):
        """Search PassiveTotal for host"""
        pass


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
        """Manage RSS feeds: rss ls, rss add <feed>, rss rm <feed>, rss watch <feed>"""
        pass


    def do_scribd(self, arg):
        """Search Scribd for active username"""
        pass

    def do_securitynews(self, arg):
        """Get current cybersecurity headlines from Google News"""
        from lib.modules import securitynews

        result = securitynews.run()

        if result is not None:
            print 'Security News:'
            for item in result['security']:
                print ('Title: %s\nURL: %s\n' % (item['title'], item['url']))

            print 'Vulnerability News:'
            for item in result['vulnerablities']:
                print ('Title: %s\nURL: %s\n' % (item['title'], item['url']))


    def do_shodan(self, arg):
        """Query Shodan for host"""
        from lib.modules import shodan

        if is_ipv4(arg) or is_ipv6(arg):
            result = shodan.ip(arg)
        elif is_fqdn(arg):
            result = shodan.domain(arg)

        if result is not None:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, {'data': {'shodan': result}})
                success('Saved Shodan results:')
            print json.dumps(result, indent=2)
        else:
            error('Failed to retrieve Shodan results: %s' % arg)


    def do_source(self, arg):
        """ Set the source for the most recent artifact added to a session """
        last = self.session.receive('artifacts')
        _type = self.check_type(last)

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
        pass


    def do_usersearch(self, arg):
        """Search Usersearch.com for active usernames"""
        pass


    def do_virustotal(self, arg):
        """Search VirusTotal for IPv4 or FQDN"""
        from lib.modules import virustotal
        if is_fqdn(arg):
            result = virustotal.run_host(arg)
            if result is not None:
                if self.db.exists('host', {'name': arg}):
                    self.db.update_one('host', {'name': arg}, {'data': {'virustotal': result}})
                    success('Saved VirusTotal results:')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get VirusTotal results (%s)' % arg)
        elif is_ipv4(arg):
            result = virustotal.run_ip(arg)
            if result is not None:
                if self.db.exists('host', {'name': arg}):
                    self.db.update_one('host', {'name': arg}, {'data': {'virustotal': result}})
                    success('Saved VirusTotal results:')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get VirusTotal results (%s)' % arg)
        else:
            warning('Virustotal command only accepts IPv4 or FQDN artifacts')


    def do_vxvault(self, arg):
        """Search VXVault for IPv4 or FQDN"""
        pass

    def do_web(self, arg):
        """Fingerprint webserver"""
        pass


    def do_whois(self, arg):
        """Perform WHOIS lookup on host"""
        from lib.modules import whois

        if is_ipv4(arg) or is_fqdn(arg):
            result = whois.run(arg)

            if result is not None:
                if self.db.exists('host', {'name': arg}):
                    self.db.update_one('host', {'name': arg}, {'data': {'whois': result}})
                    success('Saved WHOIS results:')
                print json.dumps(result, indent=2)
            else:
                warning('Failed to get WHOIS results (%s)' % arg)

        else:
            warning('Failed to get WHOIS results (%s)' % arg)


    def do_whoismind(self, arg):
        """Search Whois Mind for domains associated to an email address"""
        from lib.modules import whoismind

        result = whoismind.run(arg)
        if result is not None:
            if self.db.exists('user', {'name': arg}):
                doc_id = self.db.update_one('user', {'name': arg}, {'data': {'keybase': result}})
                if doc_id is not None:
                    success('Saved WhoisMind results:')
            print json.dumps(result, indent=2)
        else:
            warning('Failed to get WhoisMind results (%s)' % arg)


if __name__ == '__main__':
    os.system('clear')
    print asciiart.show_banner()

    parser = argparse.ArgumentParser(description='Omnibus - https://github.com/deadbits/omnibus', epilog='Your resource for all things OSINT')

    parser.add_argument('-c', '--conf',
        help='path to config file',
        action='store',
        default='%s/etc/omnibus.conf' % os.path.dirname(os.path.realpath(__file__)),
        required=False)

    parser.add_argument('-k', '--keys',
        help='path to API keys file',
        action='store',
        default='%s/etc/apikeys.json' % os.path.dirname(os.path.realpath(__file__)),
        required=False)

    parser.add_argument('-o', '--output',
        help='report output directory',
        action='store',
        default='%s/reports' % os.path.dirname(os.path.realpath(__file__)),
        required=False)

    args = parser.parse_args()

    global conf
    global output_dir
    conf = args.conf
    output = args.output

    if not os.path.exists(conf):
        error('Config file not found; exiting.')
        sys.exit(1)

    if os.path.exists(output):
        if not os.path.isdir(output):
            error('Specified output directory is not a directory; exiting.')
            sys.exit(1)
    else:
        mkdir(output)

    console = Console()
    console.cmdloop()
