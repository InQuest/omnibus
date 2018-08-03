.. _databases:

Databases
==========
Omnibus requires that MongoDB and Redis be running and reachable by the host that runs the omnibus-cli. 

The following file holds host and port configuration details for the databases. If you have them both running on your localhost and using the default ports, this config file should not need to be changed. Otherwise, edit the [mongo] and [redis] sections to your liking, ensuring to keep the file format in tact::
    etc/omnibus.conf
