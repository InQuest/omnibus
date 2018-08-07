.. _installation:

Installation
============

Omnibus Setup
-------------
Omnibus is written for Python 2.7 and has been tested on OS X 10.13.6, Ubuntu 16.04, and Ubuntu 18.04. Verify that you are on one of these operating systems, have a Python 2.7 build available, and follow the instructions below.

To get started, first clone the GitHub repository, move into the main directory, then **pip install** all required Python libraries:

.. code-block:: console

    git clone https://github.com/InQuest/omnibus
    cd omnibus
    pip install -r requirements.txt


System Pre-Requisites
---------------------
Omnibus requires that both MongoDB and Redis are running and accesible by the host that will run ``omnibus-cli.py``. These two database servers could be remote services, but connectivity must be allowed between Omnibus and these remote services. Everything on one host also works fine and is likely perferred unless you are using Omnibus in a shared user or shared investigation environment.

* Please install MongoDB by following the instructions on their official website here: `a Mongo_Installation`_. 

* Please install Redis by following the relevant instructions on their offical website `a Redis_instalation`_.


Configuration File
------------------
Omnibus provides a configuration ini file for users to change database hosts and ports at will. By modifiying the values found in ``omnibus/etc/omnibus.conf``, one can change the default hostname, port, and database name being used by both MongoDB and Redis. Below is a full default example of the **etc/omnibus.conf** file.

.. code-block:: ini

    [core]
    # history file location - leave blank if you dont wish to store any command history
    hist_file = ~/.omnibus_hist

    # number of commands to keep in history file
    hist_size = 500

    # set as 0 to only show abbreviated exceptions
    debug = 1

    # set a file path to save reports to
    # this can still be overwritten within the CLI if you wish
    reports = ../reports

    [mongo]
    host = 127.0.0.1
    port = 27017
    db = omnibus

    [redis]
    host = 127.0.0.1
    port = 6379
    db = 1


Return to Homepage
------------------
Click here to return to main documentation page: `a home`_.

.. a home: https://omnibus.readthedocs.io/en/master
.. a Mongo_Installation: https://docs.mongodb.com/manual/installation/
.. a Redis_Installation: https://redis.io/topics/quickstart

