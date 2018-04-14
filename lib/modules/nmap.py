#!/usr/bin/env python
##
# omnibus - deadbits
# nmap scanner
##
import commands


def run(host):
    results = {}
    ports = [
        '21', '22', '23', '25', '53', '80', '110', '123', '137',
        '389', '443', '445', '512', '990', '992', '993', '995', '1080', '1433',
        '3306', '3389', '5900', '5901', '5902', '5903', '6379', '6667', '6669',
        '27017']
    cmd = 'nmap -sC -sT -A -Pn -T4 -p%s %s' % (','.join(ports), host)

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
