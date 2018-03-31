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

from lib.common import is_ipv4
from lib.common import is_ipv6
from lib.common import is_fqdn
from lib.common import is_email

from lib.common import mkdir
from lib.common import error
from lib.common import running
from lib.common import success
from lib.common import warning

from lib.models import Host
from lib.models import User
from lib.models import Email


help_dict = {
    'general': ['help', 'history', 'quit', 'cat apikeys', 'add apikey'],
    'artifacts': ['cat', 'rm', 'open', 'add source', 'add note', ],
    'modules': ['abusech', 'alienvault', 'blockchain', 'clearbit', 'censys', 'cymon',
        'dnsbrute', 'dnsresolve', 'geoip', 'fullcontact', 'gist', 'gitlab', 'github', 'hackedemails', 'hibp',
        'hunter', 'ipinfo', 'ipvoid', 'isc', 'keybase', 'mdl', 'nmap', 'passivetotal', 'pastebin', 'phishtank',
        'projecthp', 'reddit', 'rss', 'scribd', 'shodan', 'ssl', 'securitynews', 'threatcrowd',
        'threatexpert', 'totalhash', 'twitter', 'urlvoid', 'usersearch', 'virustotal', 'vxvault', 'web', 'whois'],
    'sessions': ['session', 'ls', 'clear']
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
        valid_types = ['host', 'user', 'email']
        if _type in valid_types:
            return True
        return False


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
        """Show redirection command help"""
        running('Omnibus supports command redirection to output files using the ">" character. For example, "cat host zeroharbor.org > zh.json" will pipe the output of the cat command to ./zh.json on disk.')


    def do_session(self, args):
        """Open a new session"""
        self.session = cache.Cache(maxsize=self.max_session_size)
        success('Opened new session')


    def do_ls(self, arg):
        """View currently active artifacts: ls"""
        running('Active Artifacts: %s' % self.session.__len__())
        for idx, item in enumerate(self.session.__iter__()):
            print('[%d] %s' % (idx, item))


    def do_find(self, arg):
        """Find db-stored artifact by name and view results"""
        running('Searching for artifact: %s' % arg)

        if is_ipv4(arg) or is_ipv6(arg) or is_fqdn(arg):
            res = self.db.find('host', {'name': arg}, one=True)
        elif is_email(arg):
            res = self.db.find('email', {'name': arg}, one=True)
        else:
            res = self.db.find('user', {'name': arg}, one=True)

        if res:
            print json.dumps(res, indent=2)


    def do_wipe(self, arg):
        """Clear currently active artifacts: wipe"""
        running('Clearing active artifacts ...')
        for idx, item in enumerate(self.session.__iter__):
            self.session.__delitem__(idx)


    def do_rm(self, arg):
        """Remove active artifact by ID: rm <artifact id>"""
        if self.session is not None:
            if self.session.__contains__(arg):
                data = self.session.__getitem__(arg)
                self.session.__delitem__(arg)
                success('Removed artifact from cache: (%s) %s' % (arg, data))
            else:
                warning('Unable to find artifact by ID: %s' % arg)
        else:
            warning('No active session; start a new session by running the "session" command')


    def detect_type(self, arg):
        if is_ipv4(arg):
            return 'host'
        elif is_fqdn(arg):
            return 'host'
        elif is_email(arg):
            return 'email'
        else:
            return 'user'


    def do_new(self, arg):
        """Create a new artifact: new <name>"""
        _type = self.detect_type(arg)

        if _type == 'email':
            item = Email(address=arg)
        elif _type == 'host':
            item = Host(host=arg)
        elif _type == 'user':
            item = User(username=arg)
        else:
            warning('must specify one of type: email, host, user')
            return

        if not self.db.exists(_type, {'name': arg}):
            _id = self.db.insert_one(_type, item)
            if _id is not None:
                success('indexed new artifact for analysis. Mongo ID: %s' % _id)

        if self.session is not None:
            self.session = cache.Cache(maxsize=self.max_session_size)
            self.session.__setitem__(1, arg)
            success('Opened new session')
            print('Session ID: 1')
        else:
            last_id = self.session.__len__
            self.session.__setitem__(last_id + 1, arg)
            print('Session ID: %s' % last_id + 1)


    def do_delete(self, arg):
        """ Remove artifact from database by name: remove <name>"""
        _type = self.detect_type(arg)
        self.db.delete_one(_type, {'name': arg})
        self.session.__delitem__()


    def do_cat(self, arg):
        """View artifact details by type and name or list API keys: cat apikeys | cat <name>"""
        if args == 'apikeys':
            data = json.load(open(conf, 'rb'))
            print json.dumps(data, indent=2)
        else:
            _type = self.detect_type(arg)
            result = self.db.find(_type, {'name': arg}, one=True)
            if len(result) == 0:
                warning('no entry found for artifact: %s' % arg)
            else:
                print json.dumps(result, indent=2, separators=(',', ':'))


    def do_open(self, arg):
        """Load text file list of artifacts to be created: open <path/to/file.txt>"""
        if not os.path.exists(arg):
            warning('cannot find list file on disk: %s' % arg)
            return

        artifacts = open(arg, 'rb').readlines()
        for artifact in artifacts:
            if is_ipv4(artifact) or is_fqdn(artifact) or is_ipv6(artifact):
                a = Host(host=artifact)

                if not self.db.exists('host', {'name': artifact}):
                    self.db.insert_one('host', a)

            elif is_email(artifact):
                a = Email(artifact)

                if not self.db.exists('email', {'name': artifact}):
                    self.db.insert_one('email', a)

            else:
                warning('cannot determine type for artifact. treating as Username: %s' % artifact)
                a = User(artifact)

                if not self.db.exists('user', {'name': artifact}):
                    self.db.insert_one('user', a)

        success('finished loading artifact list')


    def do_report(self, arg):
        """Save JSON report for artifact: report <host|email|user> <name>"""
        parsed = self.parse_name_and_type(args)
        if parsed is None:
            return
        _type, name = parsed[0], parsed[1]

        if self.check_type(_type):
            result = self.db.find(_type, {'name': name}, one=True)
            if len(result) == 0:
                warning('no entry found for artifact: %s' % name)
            else:
                report = storage.JSON(result)
                report.save()
                if os.path.exists(report.file_path):
                    success('Saved artifact report to: %s' % report.file_path)
                else:
                    error('Failed to properly save report :(')
        else:
            warning('Must specify one of type: email, host, user')


    def do_abusech(self, arg):
        """Search Abuse.ch for artifact details"""
        pass


    def do_alienvault(self, arg):
        """Search AlienVault for artifact"""
        pass


    def do_clearbit(self, arg):
        """Search Clearbit for email address"""
        if is_email(arg):
            from lib.modules import clearbit

            result = clearbit.run(arg)
            if result:
                if self.db.exists('email', {'name': arg}):
                    self.db.update_one('email', {'name': arg}, {'clearbit': result})
                    success('saved Clearbit results to db.')
                print json.dumps(result, indent=2)
            else:
                warning('failed to get Clearbit results: %s' % arg)
        else:
            warning('failed to get Clearbit results: %s' % arg)


    def do_censys(self, arg):
        """Search Censys for IPv4 address"""
        from lib.modules import censys

        result = censys.run(arg)
        if result:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, {'clearbit': result})
                success('saved Censys.io results to db.')
            print json.dumps(result, indent=2)
        else:
            warning('failed to get Censys IPv4 results: %s' % arg)


    def do_cymon(self, arg):
        """Search Cymon for host"""
        pass


    def do_dnsbrute(self, arg):
        """Enumerate DNS subdomains of FQDN"""
        pass


    def do_dnsresolve(self, arg):
        """Retrieve DNS records for host artifact"""
        from lib.modules import dnsresolve

        result = dnsresolve.run(arg)

        if result:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, result)
                success('saved WHOIS results to db.')
            print json.dumps(result, indent=2)
        else:
            warning('failed to get WHOIS results: %s' % arg)


    def do_geoip(self, arg):
        """Retrieve Geolocation details for host"""
        from lib.modules import geoip

        result = geoip.run(arg)

        if result:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, result)
                success('saved geoIP results to db.')
            print json.dumps(result, indent=2)
        else:
            warning('failed to get freegeoip results: %s' % arg)


    def do_fullcontact(self, arg):
        """Search FullContact for email address"""
        pass


    def do_gist(self, arg):
        """Search Github Gist's for artifact as string"""
        pass


    def do_gitlab(self, arg):
        """Check Gitlab for active username"""
        pass


    def do_github(self, arg):
        """Check GitHub for active username"""
        pass


    def do_hackedemails(self, arg):
        """Check hacked-emails.com for email address"""
        pass


    def do_hibp(self, arg):
        """Check HaveIBeenPwned for email address"""
        pass


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
                    doc_id = self.db.update_one('host', {'name': arg}, {'isc': result})
                    if doc_id is not None:
                        success('saved SANS ISC results:')
                print json.dumps(result, indent=2)
            else:
                warning('failed to get SANS ISC results: %s' % arg)
        else:
            warning('must specify IPv4 or FQDN artifact: %s' % arg)


    def do_keybase(self, arg):
        """Search Keybase for active username"""
        pass


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
                    self.db.update_one('host', {'name': arg}, {'nmap': result})
                    success('saved Nmap results to db.')
                for item in result['ports']:
                    print item
            else:
                warning('nmap scan completed but no open ports found')
        else:
            error('must specify a IPv4 or FQDN artifact')


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
                print ('title: %s\nurl: %s\n' % (item['title'], item['url']))

            print 'Vulnerability News:'
            for item in result['vulnerablities']:
                print ('title: %s\nurl: %s\n' % (item['title'], item['url']))


    def do_shodan(self, arg):
        from lib.modules import shodan

        if is_ipv4(arg) or is_ipv6(arg):
            result = shodan.ip(arg)
        elif is_fqdn(arg):
            result = shodan.domain(arg)

        if result is not None:
            if self.db.exists('host', {'name': arg}):
                self.db.update_one('host', {'name': arg}, result)
                success('saved Shodan results to db.')
            print json.dumps(result, indent=2)
        else:
            error('failed to retrieve Shodan results: %s' % arg)


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
                success('saved VirusTotal results:')
                print json.dumps(result, indent=2)
            else:
                warning('failed to get VirusTotal results: %s' % arg)
        elif is_ipv4(arg):
            result = virustotal.run_ip(arg)
            if result is not None:
                success('saved VirusTotal results:')
                print json.dumps(result, indent=2)
            else:
                warning('failed to get VirusTotal results: %s' % arg)
        else:
            warning('virustotal command only accepts IPv4 or FQDN artifacts')


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
                success('saved WHOIS result:')
                print json.dumps(result, indent=2)
            else:
                warning('failed to get WHOIS results: %s' % arg)

        else:
            warning('failed to get WHOIS results: %s' % arg)


if __name__ == '__main__':
    os.system('clear')
    parser = argparse.ArgumentParser(description='Omnibus - https://github.com/deadbits/omnibus', epilog='Your resource for all things OSINT')

    parser.add_argument('-c', '--conf',
        help='path to config file',
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
        error('config file not found; exiting.')
        sys.exit(1)

    if os.path.exists(output):
        if not os.path.isdir(output):
            error('specified output directory is not a directory; exiting.')
            sys.exit(1)
    else:
        mkdir(output)

    console = Console()
    console.cmdloop()
