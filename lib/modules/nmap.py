#!/usr/bin/env python
##
# omnibus - deadbits
# nmap scanner
##
import commands


def run(host):
    results = {}

    cmd = 'nmap -sC -sT -A -Pn -T4 - %s' % host

    try:
        out = commands.getoutput(cmd)
        for line in out.splitlines():
            if 'tcp' in line and 'open' in line:
                open_port = line.split('/tcp')[0]
                results['ports'].append(open_port)
    except:
        pass

    return results


def main(artifact, artifact_type=None):
    result = run(artifact)
    return result
