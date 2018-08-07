.. _redirection:

Redirection
============
The output of commands can also be saved to arbitrary text files using the standard Linux character >. For example, if you wish to store the output of a VirusTotal lookup for a host to a file called "vt-lookup.json" you would simply execute:

``virustotal inquest.net > vt-lookup.json``

By default the redirected output files are saved in the current working directory, therefore "omnibus/", but if you specify a full path such as

``virustotal inquest.net > /home/adam/intel/cases/001/vt-lookup.json``

The JSON formatted output will be saved to the specified path.
