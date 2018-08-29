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

After installing the pre-reqs exlplained in the next step, simply run ``python2.7 omnibus-cli.py``.
It is recommended to start the CLI script with the ``--debug`` argument in order to see full Python tracebacks should any errors occur and you need to report a bug on the GitHub repo.

.. code-block::

    user:~/omnibus $ python2.7 omnibus-cli.py --debug

     ██████╗ ███╗   ███╗███╗   ██╗██╗██████╗ ██╗   ██╗███████╗
    ██╔═══██╗████╗ ████║████╗  ██║██║██╔══██╗██║   ██║██╔════╝
    ██║   ██║██╔████╔██║██╔██╗ ██║██║██████╔╝██║   ██║███████╗
    ██║   ██║██║╚██╔╝██║██║╚██╗██║██║██╔══██╗██║   ██║╚════██║
    ╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║██████╔╝╚██████╔╝███████║
     ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚═════╝  ╚═════╝ ╚══════╝
                 https://github.com/InQuest/omnibus


    [*] Using configuration file (/home/user/omnibus/etc/omnibus.conf) ...
    [*] Debug: True
    debug - was: False
    now: True
    Welcome to the Omnibus shell! Type "session" to get started or "help" to view all commands.
    omnibus >>

You can also set the ``debug`` flag after you start the Omnibus console by running ``set debug true``.

.. code-block::

    [*] Using configuration file (/Users/adam/Desktop/omnibus/etc/omnibus.conf) ...
    [*] Debug: False
    Welcome to the Omnibus shell! Type "session" to get started or "help" to view all commands.
    omnibus >> set debug true
    debug - was: False
    now: True
    omnibus >> 


System Pre-Requisites
---------------------
Omnibus requires that both MongoDB and Redis are running and accesible by the host that will run ``omnibus-cli.py``.

These two database servers could be remote services, but connectivity must be allowed between Omnibus and these remote services. Everything on one host also works fine and is likely perferred unless you are using Omnibus in a shared user or shared investigation environment.

**Installation or support for these two services is out of scope for this documentation: please refer to the official guides linked below**

* Install MongoDB using instructions on their official website: https://docs.mongodb.com/manual/installation/ 
* Install Redis using instructions on their offical website: https://redis.io/topics/quickstart


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

