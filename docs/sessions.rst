.. _sessions:

Sessions
==========
Omnibus makes use of a feature called "sessions". Sessions are temporary caches created using Redis that start with each new CLI session. These session caches are cleared from Redis when you exit ``omnibus-cli.py`` using the ``quit`` command. If you do not exit the application this way, your next session will still include your previous sessions artifacts. TL;DR Please use ``quit`` to close the application unless you want all that data in Redis :)

Interacting with Session IDs
----------------------------
Sessions are here for easy access to artifacts and will be cleared each time you quit the command line session. If you wish to clear the session early, run the command "wipe" and you'll get a clean slate.

Every time you create an artifact, that artifacts name is added to the Session along with a numeric key that makes for easy retrieval, searching, and action against the related artifact.

For example if you're session held one item of "inquest.net", instead of needing to execute ``virustotal inquest.net`` you could also run ``virustotal 1`` and you would receive the same results. 

In fact, this works against any module or command that uses an artiface name as it's first argument.

Return to Homepage
------------------
Click here to return to main documentation page: `a home`_.

.. a home: https://omnibus.readthedocs.io/en/master
