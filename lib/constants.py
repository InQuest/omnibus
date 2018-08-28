#!/usr/bin/env python
# -*- coding: utf-8 -*-
##
# App: Omnibus - InQuest Labs
# Website: https://www.inquest.net
# Author: Adam M. Swanda
# ---
# [IMPORTANT] DO NOT CHANGE THESE VARIABLES!
# - The entire app relies on knowing the root_path, api_keys, and app_conf locations
# - The build_version and app_version are critical for InQuest to debug any issues you might have.
# - If you *have* changed these, we very likely won't be able to accurately debug your issue and you may be on your own :|
#       - For real.. don't change them.
##

import os
import subprocess

__app_stage = 'beta'
__app_major = '1.0'

__cwd = os.path.abspath(os.path.dirname(__file__))

root_path = os.path.abspath(os.path.join(__cwd, '..'))
api_keys = os.path.join(root_path, 'etc/apikeys.json')
app_conf = os.path.join(root_path, 'etc/omnibus.conf')

rev_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
rev_count = subprocess.check_output(["git", "rev-list", "HEAD", "--count"])

build_version = 'v{}.{}-{}_{}'.format(__app_major, rev_count.strip(), rev_hash.strip(), __app_stage)
app_version = 'v{}.{}_{}'.format(__app_major, rev_count.strip(), __app_stage)

# example output:
# build: v1.0.125-e73bcf8_beta
# app: v1.0.125_beta
