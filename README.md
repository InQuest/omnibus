# OSINT Omnibus
- Developed & maintained by [InQuest](https://www.inquest.net)
- ![Release](https://img.shields.io/badge/Release-Beta-blue.svg)
- [![Rawsec's CyberSecurity Inventory](http://list.rawsec.ml/img/badges/Rawsec-inventoried-FF5050_flat_without_logo.svg)](http://list.rawsec.ml/tools.html#Omnibus)


Table of Contents
===============================

* [OSINT Omnibus](#osint-omnibus)
  * [Omnibus](#omnibus)
    * [Documentation](#documentation)
    * [Vocabulary](#vocabulary)
    * [Running Omnibus](#running-omnibus)
      * [API Keys](#api-keys)
    * [Interactive Console](#interactive-console)
    * [Artifacts](#artifacts)
      * [Overview](#overview)
      * [Creating &amp; Managing Artifacts](#creating--managing-artifacts)
    * [Sessions](#sessions)
    * [Modules](#modules)
    * [Machines](#machines)
    * [Reporting](#reporting)
    * [Monitoring Modules](#monitoring-modules)

# OSINT Omnibus
- Developed & maintained by [InQuest](https://www.inquest.net)
- ![Release](https://img.shields.io/badge/Release-Beta-blue.svg)
- [![Rawsec's CyberSecurity Inventory](http://list.rawsec.ml/img/badges/Rawsec-inventoried-FF5050_flat_without_logo.svg)](http://list.rawsec.ml/tools.html#Omnibus)


## Omnibus
An Omnibus is defined as `a volume containing several novels or other items previously published separately` and that is exactly what the InQuest Omnibus project intends to be for Open Source Intelligence collection, research, and artifact management.

By providing an easy to use interactive command line application, users are able to create sessions to investigate various artifacts such as IP addresses, domain names, email addresses, usernames, file hashes, Bitcoin addresses, and more as we continue to expand.

This project has taken motivation from the greats that came before it such as SpiderFoot, Harpoon, and DataSploit. Much thanks to those great authors for contributing to the world of open source.

The application is written with Python 2.7 in mind and has been successfully tested on OSX and Ubuntu 16.04 environments.

This is a beta of the final application and as such there may be some bugs or other weirdness during usage. For the most part Omnibus is fully functional and can be used to begin OSINT investigation right away.

### Contribution
Omnibus is built in a modular manner that allows the easy addition of OSINT data source modules and import/export modules. Each module per category is included in a single directory, and by adding a few lines of code, your module could be the next!

As the Wiki continues to grow, we will have full examples of how to write custom plugins.

If you happen to notice any bugs or other issues, please create an Issue and/or Pull Request. We would also love for community support in creating more modules and expanding the Omnibus use-cases. Forks and Pull Requests for new features are more than welcome!

### Documentation
This README file serves as a quick overview of Omnibus and its features. Full documentation is available in the 'docs' folder of this repository.

### Vocabulary
Before we begin we'll need to cover some terminology used by Omnibus.

* Artifact:
  - An item to investigate
  - Artificats can be created in two ways:
    - Using the `new` command or by being discoverd through module execution
* Session:
  - Cache of artifacts created after starting the Omnibus CLI
  - Each artifact in a session is given an ID to quickly identify and retrieve the artifact from the cache
  - Commands can be executed against an artifact either by providing it's name or it's corresponding session ID
* Module:
  - Python script that performs some arbitirary OSINT task against an artifact

### Running Omnibus
Starting up Omnibus for investigation is a simple as cloning this GitHub repository, installing the Python requirements using `pip install -r requirements.txt` and running `python omnibus-cli.py`.

**Omnibus Shell - Main Startup**
![Alt text](docs/images/omnishell.png?raw=true "Shell")

For a visual reference of the CLI, pictured above is the Omnibus console after a new session has been started, 2 artifacts have been added to a session, and the `help` menu is shown.

#### API Keys
You must set any API keys you'd like to use within modules inside the `omnibus/etc/apikeys.json` file.
This file is a JSON ocument with placeholders for all the services which require API keys, and is only accessed by Omnibus on a per module basis to retrieve the exact API key a module needs to execute.

It should be noted that most of the services requiring API keys have free accounts and API keys. Some free accounts may have lower resource limits, but that hasn't been a problem during smaller daily investigations or testing the application.

**A handy tip**: Use the `cat apikeys` command to view which keys you do in fact have stored.
If modules are failing or returning no results, check here first to ensure your API key is properly saved.

### Interactive Console
When you first run the CLI, you'll be greeted by a help menu with some basic information.
Omnibus tries to use commands that mimic some common Linux commands for familiarity and ease of use. For example, the command `cat` to show information about and artifact, `rm` to remove an artifact from the database, `ls` for view current session artifacts, and output redirection support for any command using the `>` character.

As an example of output redirection, if you wish to retrieve the details of an artifact named "inquest.net" saved to a JSON file on your local disk you'd simply run the command:
`cat inquest.net > inquest-report.json` and there it would be! 
This feature also works with full file paths instead of relative paths.

The high level commands used in Omnibus most often are:
* `session`
  - start a new session
* `new <artifact name>`
  - create a new artifact for investigation
* `modules`
  - display list of available modules
* `open <file path>`
  - load a text file list of artifacts into Omnibus as artifacts
* `ls`
  - show all active artifacts
* `rm`
  - remove an artifact from the database
* `wipe`
  - clear the current artifact session
* `cat <artifact name | session id>`
  - view beautified JSON database records
* `<module name> <artifact name | session id>`
  - run a module against an artifact to view & store the results
  - newly discovered artifacts from a modules executed are added as children to the original artifact and created in the database as their own new artifacts
* `<machine name> <artifact name | session id>`
  - run all modules for an artifacts type against the specified artifact
  - all results are displayed in the output and stored to the database
  - provides an easy method to collect bulk information all at once

If you ever need a quick reference on the different commands available for different areas of the application there are sub-help menus for this exact purpose. Using these commands will show you only those commands available relevant to a specific area:
* `general`
  - overall commands such as help, history, quit, set, clear, banner, etc.
* `artifacts`
  - display commands specific to artifacts and their management
* `sessions`
  - display helpful commands around managing sessions
* `modules`
  - show a list of all available modules

### Artifacts
#### Overview
Most cyber investigations begin with one or more technical indicators, such as an IP address, file hash or email address. After searching and analyzing, relationships begin to form and you can pivot through connected data points. These data points are called Artifacts within Omnibus and represent any item you wish to investigate.

Artifacts can be one of the following types:
* IPv4 address
* FQDN
* Email Address
* Bitcoin Address
* File Hash (MD5, SHA1, SHA256, SHA512)
* User Name

#### Creating & Managing Artifacts
The command "new" followed by an artifact will create that artifact within your Omnibus session and store a record of the artifact within MongoDB. This record holds the artifact name, type, subtype, module results, source, notes, tags, children information (as needed) and time of creation.
Every time you run a module against a created or stored artifact, the database document will be updated to reflect the newly discovered information.

To create a new artifact and add it to MongoDB for tracking, run the command `new <artifact name>`. For example, to
start investigation the domain inquest.net, you would run `new inquest.net`.

Omnibus will automatically determine what type the artifact is and ensure that only modules for that type are executed against the artifact. _If you attempt to run an artifact against a module that cannot support the artifact type, you'll be notified by a warning message that lists the accepted types._

When a module is created, new artifacts may be found during the discovery process. For example, running the "dnsresolve" command might find new IPv4 addresses not previously seen by Omnibus. If this is the case, those newly found artifacts are automatically created as new artifacts in Omnibus and linked to their parent with an additional field called "source" to identify from which module they were originally found. In this example the source of the newly created artifacts would be "dnsresolve".

Artifacts can be removed from the database using the "rm" command. If you no longer need an artifact, simply run the delete command and specify the artifacts name or the session ID if it has one.

### Sessions
Omnibus makes use of a feature called "sessions". Sessions are temporary caches created via Redis each time you start a CLI session. Every time you create an artifact, that artifacts name is added to the Session along with a numeric key that makes for easy retrieval, searching, and action against the related artifact.
For example if you're session held one item of "inquest.net", instead of needing to execute `virustotal inquest.net` you could also run `virustotal 1` and you would receive the same results. In fact, this works against any module or command that uses an artiface name as it's first argument.

**Interacting with Session IDs instead of Artifact names**
![Alt text](docs/images/artifact_id.png?raw=true "Shell")

Sessions are here for easy access to artifacts and will be cleared each time you quit the command line session.
If you wish to clear the session early, run the command "wipe" and you'll get a clean slate.

### Modules
Omnibus currently supports the following list of modules. If you have suggestions or modules or would like to write one
of your own, please create a pull request.

Also, within the Omnibus console, typing the module name will show you the Help information associated with that module.

**Modules**
* Blockchain.info
* Censys
* ClearBit
* CSIRTG
* Cymon
* DNS resolution
* DShield (SANS ISC)
* Full Contact
* Geolocation
* GitHub username search
* HackedEmails.com
* HaveIBeenPwned.com
* Hurricane Electric
* IPInfo
* IPVoid
* Keybase username lookup
* NMap scanner
* OTX (AlienVault)
* PassiveTotal
* PGP Key Search
* RSS reader 
* Shodan
* ThreatCrowd
* ThreatExpert
* Twitter
* URLVoid
* VirusTotal
* WHOIS
* WhoisMind

### Machines
Machines are a simple way to run all available modules for an artifact type against a given artifact. This is a fast way if you want to gather as much information on a target as possible using a single command.

To perform this, simply run the command `machine <artifact name|session ID>` and wait a few minutes until the modules are finished executing.

The only caveat is that this may return a large volume of data and child artifacts depending on the artifact type and the results per module. To remedy this, we are investigating a way to remove specific artifact fields from the stored database document to make it easier for users to prune unwanted data.

### Quick Reference Guide
Some quick commands to remember are:
- `session` - start a new artifact cache
- `cat <artifact name>|apikeys` - pretty-print an artifacts document or view your stored API keys
- `open <file path>` - load a text file list of artifacts into Omnibus for investigation
- `new <artifact name>` - create a new artifact and add it to MongoDB and your session
- `find <artifact name>` - check if an artifact exists in the db and show the results


### Reporting
Reports are the JSON output of an artifacts database document, essentially a text file version of the output of the "cat" command. But by using the `report` command you may specify an artifact and a filepath you wish to save the output to:
* `omnibus >> report inquest.net /home/adam/intel/osint/reports/inq_report.json`

This above command overrides the standard report directory of `omnibus/reports`. By default, and if you do not specify a report path, all reports will be saved to that location. Also, if you do not specify a file name the report will use the following format:
* `[artifact_name]_[timestamp].json`

#### Redirection
The output of commands can also be saved to arbitrary text files using the standard Linux character `>`.
For example, if you wish to store the output of a VirusTotal lookup for a host to a file called "vt-lookup.json" you would simply execute:
* `virustotal inquest.net > vt-lookup.json`

By default the redirected output files are saved in the current working directory, therefore "omnibus/", but if you specify a full path such as `virustotal inquest.net > /home/adam/intel/cases/001/vt-lookup.json` the JSON formatted output will be saved there.

