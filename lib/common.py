#!/usr/bin/env python
import os
import re
import sys
import json
import requests
import datetime
import warnings
import functools

from requests.packages.urllib3 import exceptions


jsondate = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None

# regex patterns courtesy of https://github.com/yolothreat/utilitybelt
re_ipv4 = re.compile('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', re.I | re.S | re.M)
re_ipv6 = re.compile('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))', re.I | re.S | re.M)
re_email = re.compile("\\b[A-Za-z0-9_.]+@[0-9a-z.-]+\\b", re.I | re.S | re.M)
re_fqdn = re.compile('(?=^.{4,255}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)', re.I | re.S | re.M)
re_cve = re.compile("(CVE-(19|20)\\d{2}-\\d{4,7})", re.I | re.S | re.M)
re_url = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.I | re.S | re.M)
re_md5 = re.compile("\\b[a-f0-9]{32}\\b", re.I | re.S | re.M)
re_sha1 = re.compile("\\b[a-f0-9]{40}\\b", re.I | re.S | re.M)
re_sha256 = re.compile("\\b[a-f0-9]{64}\\b", re.I | re.S | re.M)
re_sha512 = re.compile("\\b[a-f0-9]{128}\\b", re.I | re.S | re.M)

BOLD = "\033[1m"
GREY = '\033[90m'
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
LIGHTBLUE = '\033[96m'
END_COLOR = '\033[0m'

CONF = '../etc/apikeys.json'


def info(msg):
    print('%s%s[*]%s %s' % (BOLD, LIGHTBLUE, END_COLOR, msg))


def running(msg):
    print('%s%s[*]%s %s' % (BOLD, GREY, END_COLOR, msg))


def success(msg):
    print('%s%s[~]%s %s' % (BOLD, GREEN, END_COLOR, msg))


def warning(msg):
    print('%s%s[!]%s %s' % (BOLD, YELLOW, END_COLOR, msg))


def error(msg):
    print('%s%s[!]%s %s' % (BOLD, RED, END_COLOR, msg))


@functools.wraps
def ignore_warnings(function):
    def _ignore_warning(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = function(*args, **kwargs)
        return result
    return _ignore_warning


def get_apikey(service):
    if os.path.exists(CONF):
        data = load_json(CONF)
        if service in data.keys():
            return data[service]
    else:
        error('cannot find API keys file: %s' % CONF)


def timestamp():
    return datetime.datetime.isoformat(datetime.datetime.utcnow())


def required_opt(argument):
    error('argument %s is required!' % argument)
    sys.exit(1)


def list_dir(directory):
    files = []
    for root, dirs, files in os.walk(directory, topdown=True):
        files = [f for f in files if not f[0] == '.']
        for _file in files:
            files.append(os.path.join(root, _file))
    return files


def write_file(file_path, data):
    try:
        with open(file_path, 'a+') as fp:
            fp.write(data)
        return True
    except Exception as err:
        raise err
        return False


def read_file(file_path, lines=False):
    if is_valid(file_path):
        if lines:
            _data = (open(file_path, 'rb').read()).split('\n')
        else:
            _data = open(file_path, 'rb').read()
        return _data
    return False


def load_json(file_name):
    if is_valid(file_name):
        return json.load(open(file_name, 'rb'))
    return None


def is_valid(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path) \
            and os.path.getsize(file_path) > 0:
        return True
    return False


def mkdir(path):
    if os.path.isdir(path):
        return True
    else:
        try:
            os.mkdir(path)
            os.chmod(path, 0777)
            return True
        except:
            return False


def http_post(*args, **kwargs):
    """ Wrapped to silently ignore certain warnings from urllib3 library """
    kwargs['verify'] = False
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
        warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
        req = requests.get(*args, **kwargs)
        if req.status_code == 200:
            return (True, req)
        else:
            return (False, req)


def http_get(*args, **kwargs):
    """ Wrapped to silently ignore certain warnings from urllib3 library """
    kwargs['verify'] = False
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', exceptions.InsecureRequestWarning)
        warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)
        req = requests.get(*args, **kwargs)
        if req.status_code == 200:
            return (True, req)
        else:
            return (False, req)


def is_ipv4(ipv4address):
    return bool(re.match(re_ipv4, ipv4address))


def is_ipv6(ipv6address):
    return bool(re.match(re_ipv6, ipv6address))


def is_fqdn(address):
    return bool(re.match(re_fqdn, address))


def is_url(url):
    return bool(re.match(re_url, url))


def is_email(address):
    return bool(re.match(re_email, address))


def is_hash(string):
    if re.match(re_md5, string):
        return 'md5'
    elif re.match(re_sha1, string):
        return 'sha1'
    elif re.match(re_sha256, string):
        return 'sha256'
    elif re.match(re_sha512, string):
        return 'sha512'
    else:
        return False
