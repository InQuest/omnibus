#!/usr/bin/env python
##
# omnibus
# argparse helpers for cmd2 cli
##

import argparse

# do_tags parsere
tags_parser = argparse.ArgumentParser()
id_tags = tags_parser.add_mutually_exclusive_group()
manage_tags = tags_parser.add_mutually_exclusive_group()

manage_tags.add_argument('-a', '--add', action='store_true', help='add tag')
manage_tags.add_argument('-v', '--view', action='store_true', help='view tags')

id_tags.add_argument('-l', '--last', action='store_true', help='use last created artifact')
id_tags.add_argument('-n', '--name', action='store', help='artifact name')
id_tags.add_argument('-i', '--id', action='store', help='artifact session ID')

tags_parser.add_argument('tags', nargs='?', help='comma separated tags')


# do_source parser
source_parser = argparse.ArgumentParser()
id_source = source_parser.add_mutually_exclusive_group()
manage_source = source_parser.add_mutually_exclusive_group()

manage_source.add_argument('-a', '--add', action='store_true', help='add source')
manage_source.add_argument('-v', '--view', action='store_true', help='view source')

id_source.add_argument('-l', '--last', action='store_true', help='use last created artifact')
id_source.add_argument('-n', '--name', action='store', help='artifact name')
id_source.add_argument('-i', '--id', action='store', help='artifact session ID')

source_parser.add_argument('source', nargs='?', help='source value')


# do_session parser
session_parser = argparse.ArgumentParser()
manage_session = session_parser.add_mutually_exclusive_group()
manage_session.add_argument('-n', '--new', action='store_true', help='open a new session')
manage_session.add_argument('-c', '--clear', action='store_true', help='clear current session')
manage_session.add_argument('-v', '--view', action='store_true', help='view session artifacts')
manage_session.add_argument('-d', '--delete', action='store', help='remove artifact from session by name or ID')


# do_artifact parser
artifact_parser = argparse.ArgumentParser()
manage_artifact = artifact_parser.add_mutually_exclusive_group()
manage_artifact.add_argument('-n', '--new', action='store_true', help='create or open an artifact')
manage_artifact.add_argument('-v', '--view', action='store_true', help='view stored artifact data')
manage_artifact.add_argument('-r', '--report', action='store_true', help='save artifact data as JSON report')
manage_artifact.add_argument('-d', '--delete', action='store_true', help='delete an artifact from database')
artifact_parser.add_argument('artifact', nargs='+', help='artifact name')
