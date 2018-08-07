.. _machines:

Machines
========
Machines are a simple way to run all available modules for an artifact type against a given artifact. This is a fast way if you want to gather as much information on a target as possible using a single command.

To perform this, simply run the command ``machine <artifact name|session ID>`` and wait a few minutes until the modules are finished executing.

The only caveat is that this may return a large volume of data and child artifacts depending on the artifact type and the results per module. To remedy this, we are investigating a way to remove specific artifact fields from the stored database document to make it easier for users to prune unwanted data.
