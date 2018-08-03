.. Omnibus documentation master file, created by
   sphinx-quickstart on Fri Aug  3 14:19:10 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

OSINT Omnibus
===================================

Omnibus is an easy to user interactive command line applications for users to perform OSINT investigation of artifacts such as IP addresses, domains, email addresses, user names, file hashes, and Bitcoin addresses.

An Omnibus is defined as a volume containing several novels or other items previously published separately and that is exactly what the InQuest Omnibus project intends to be for Open Source Intelligence collection, research, and artifact management.

The project requires both MongoDB and Redis running in order to store artifact data long term and while within a CLI session, respectively.

User Guide
----------

- Getting Started

 .. toctree::
    :maxdepth: 2
    
    installation
    databases
    apikeys
    vocabulary

- Using Omnibus

 .. toctree::
    :maxdepth: 2

    interactivecli
    artifacts
    sessions
    modules
    machines
    reporting
    redirection

- Quick Reference

 .. toctree::
    :maxdepth: 2

    quickref

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
