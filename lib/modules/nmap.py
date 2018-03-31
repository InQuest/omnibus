#!/usr/bin/env python
##
# omnibus - deadbits
# nmap scanner
##
import commands


def run(host):
    results = {'ports': []}
    cmd = 'nmap -sT -sV -Pn -T5 -p21,22,23,25,80,443,993,8080,6667,3306,3389 %s' % host

    try:
        out = commands.getoutput(cmd)
        for line in out.splitlines():
            if 'tcp' in line and 'open' in line:
                results['ports'].append(line.strip())
    except:
        pass

    return results
