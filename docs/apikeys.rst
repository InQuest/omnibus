.. _api_keys:


API Keys
========

Setting Up Your API Keys
------------------------

You must set any API keys you'd like to use within modules inside the ``omnibus/etc/apikeys.json`` file. This file is a JSON document with placeholders for all the services which require API keys, and is only accessed by Omnibus on a per module basis to retrieve the exact API key a module needs to execute.

It should be noted that most of the services requiring API keys have free accounts and API keys. Some free accounts may have lower resource limits, but that hasn't been a problem during smaller daily investigations or testing the application.

A handy tip: Use the ``cat apikeys`` command to view which keys you do in fact have stored. If modules are failing or returning no results, check here first to ensure your API key is properly saved.

Users will require API keys for the following modules/services:

* Censys
* ClearBit
* CSIRTG
* IPStack
* FullContact
* Shodan
* SecurityTrails
* MalwarePatrol
* PassiveTotal
* VirusTotal

The default empty ``apikeys.json`` file can be seen below.

.. code-block:: json

       {
           "censys": {
               "token": "",
               "secret": ""
           },
           "clearbit": "",
           "csirtg": "",
           "ipstack": "",
           "fullcontact": "",
           "shodan": "",
           "securitytrails": "",
           "malwarepatrol": "",
           "passivetotal": {
             "user": "",
             "key": ""
           },
           "virustotal": ""
       }


Return to Homepage
------------------
Click here to return to main documentation page: `a home`_.

.. a home: https://omnibus.readthedocs.io/en/master
