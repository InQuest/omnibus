.. _reporting:

Reporting
==========

Reports are the JSON output of an artifacts database document, essentially a text file version of the output of the ``cat`` command. But by using the report command you may specify an artifact and a filepath you wish to save the output to:

``report inquest.net /home/adam/intel/osint/reports/inq_report.json``

This above command overrides the standard report directory of omnibus/reports. By default, and if you do not specify a report path, all reports will be saved to that location.

Also, if you do not specify a file name the report will use the following format:

``[artifact_name]_[timestamp].json``

In upcoming Omnibus versions you will be able to run arbitrary search queries and store a report on all hits for that search.
