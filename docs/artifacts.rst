.. _artifacts:

Artifacts
==========

Artifact Overview
-----------------
Most cyber investigations begin with one or more technical indicators, such as an IP address, file hash or email address. After searching and analyzing, relationships begin to form and you can pivot through connected data points. These data points are called Artifacts within Omnibus and represent any item you wish to investigate.

Artifacts can be one of the following types:

* IPv4 address
* FQDN
* Email Address
* Bitcoin Address
* File Hash (MD5, SHA1, SHA256, SHA512)
* User Name

Creating & Managing Artifacts
-----------------------------
The command ``new`` followed by an artifact will create that artifact within your Omnibus session and store a record of the artifact within MongoDB. This record holds the artifact name, type, subtype, module results, source, notes, tags, children information (as needed) and time of creation. Every time you run a module against a created or stored artifact, the database document will be updated to reflect the newly discovered information.

To create a new artifact and add it to MongoDB for tracking, run the command new <artifact name>. For example, to start investigation the domain inquest.net, you would run ``new inquest.net``.

Omnibus will automatically determine what type the artifact is and ensure that only modules for that type are executed against the artifact. If you attempt to run an artifact against a module that cannot support the artifact type, you'll be notified by a warning message that lists the accepted types.

When a module is created, new artifacts may be found during the discovery process. For example, running the ``dnsresolve`` command might find new IPv4 addresses not previously seen by Omnibus. If this is the case, those newly found artifacts are automatically created as new artifacts in Omnibus and linked to their parent with an additional field called ``source`` to identify from which module they were originally found. In this example the source of the newly created artifacts would be ``dnsresolve``.

Artifacts can be removed from the database using the ``rm`` command. If you no longer need an artifact, simply run the delete command and specify the artifacts name or the session ID if it has one.


Return to Homepage
------------------
Click here to return to main documentation page: `a home`_.


.. a home: https://omnibus.readthedocs.io/en/master
