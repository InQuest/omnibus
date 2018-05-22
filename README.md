# OSINT Omnibus
![Release](https://img.shields.io/badge/Release-Alpha-blue.svg)
Provided by [InQuest](https://www.inquest.net)

Table of Contents
=================

* [OSINT Omnibus](#osint-omnibus)
  * [Omnibus](#omnibus)
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
![Release](https://img.shields.io/badge/Release-Alpha-blue.svg)

Provided by [InQuest](https://www.inquest.net)

There will be some bugs as this is a very early release of the application (pre-alpha). If you do happen to notice any modules that fail or other bugs, please create an Issue and/or Pull Request. Both are more than welcome as we'd love to expand this framework as we go on!

## Omnibus
An Omnibus is defined as `a volume containing several novels or other items previously published separately` and that is exactly what the InQuest Omnibus project intends to be for Open Source Intelligence collection, research, and artifact management.

By providing an easy to use interactive command line application, users are able to create sessions to investigate various artifacts such as IP addresses, domain names, email addresses, usernames, file hashes, Bitcoin addresses, and more as we continue to expand.

This project has taken motivation from the greats that came before it such as SpiderFoot, Harpoon, and DataSploit. Much thanks to those great authors for contributing to the world of open source.

The application is written with Python 2.7 in mind and has been successfully tested on OSX and Ubuntu 16.04 environments.

As this is a pre-release of the final application, there will very likely be some bugs and uncaught exceptions or other weirdness during usage. Though for the most part, it is fully functional and can be used to begin OSINT investigations right away.

### Contribution
Omnibus is built in a modular manner that allows the easy addition, or removal, of OSINT plugins. Each module is included in a single directory, and by adding a few lines of code, your module could be the next one!

As this README and the Wiki continues to grow, we will have full-fledged examples of how to write custom plugins and get them in as Pull Requests!

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
Starting up Omnibus for investigation is a simple as cloning this GitHub repository, installing the Python requirements using `pip install -r requirements.txt` and running `python2.7 omnibus-cli.py`.

**Omnibus Shell - Main Startup**
![Alt text](docs/images/omnishell.png?raw=true "Shell")

For a visual reference of the CLI, pictured above is the Omnibus console after a new session has been started, 2 artifacts have been added to a session, and the `help` menu is shown.

#### API Keys
You must set any API keys you'd like to use within modules inside the `omnibus/etc/apikeys.json` file.
This file is a JSON ocument with placeholders for all the services which require API keys, and is only accessed by Omnibus on a per module basis to retrieve the exact API key a module needs to execute.

It should be noted that most of the services requiring API keys have free accounts and API keys. Some free accounts may have lower resource limits, but that hasn't been a problem during smaller daily investigations or testing the application.

**A handy tip**: Use the `cat apikeys` command to view which keys you do in fact have stored.
If modules are failing, check here first to ensure your API key is properly saved.

### Interactive Console
When you first run the CLI, you'll be greeted by a help menu with some basic information. We tried to build the command line script to mimic some common Linux console commands for ease of use. Omnibus provides commands such as `cat` to show information about an artifact, `rm` to remove an artifact from the database, `ls` to view currently session artifacts, and so on.

One additional feature of note is the use of the `>` character for output redirection. For example, if you wish to retrieve the details of an artifact named "inquest.net" saved to a JSON file on your local disk you'd simply run the command:
`cat inquest.net > inquest-report.json` and there it would be! This feature also works with full file paths instead of relative paths.

The high level commands you really need to know to use Omnibus are:
* `session`
  - start a new session
* `new <artifact name>`
  - create a new artifact for investigation
* `modules`
  - display list of available modules
* `open <file path>`
  - load a text file list of artifacts into Omnibus as artifacts
* `cat <artifact name | session id>`
  - view beautified JSON database records
* `ls`
  - show all active artifacts
* `rm`
  - remove an artifact from the database
* `wipe`
  - clear the current artifact session

Also, if you ever need a quick reference on the different commands available for different areas of the application there are sub-help menus for this exact purpose. Using these commands will show you only those commands available relevant to a specific area:
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
start investigation the domain deadbits.org, you would run `new deadbits.org`.

Omnibus will automatically determine what type the artifact is and ensure that only modules for that type are executed against the artifact.

When a module is created, new artifacts may be found during the discovery process. For example, running the "dnsresolve" command might find new IPv4 addresses not previously seen by Omnibus. If this is the case, those newly found artifacts are automatically created as new artifacts in Omnibus and linked to their parent with an additional field called "source" to identify from which module they were originally found.

Artifacts can be removed from the database using the "delete" command. If you no longer need an artifact, simply run the delete command and specify the artifacts name or the session ID if it has one.

### Sessions
Omnibus makes use of a feature called "sessions". Sessions are temporary caches created via Redis each time you start a CLI session. Every time you create an artifact, that artifacts name is added to the Session along with a numeric key that makes for easy retrieval, searching, and action against the related artifact.
For example if you're session held one item of "inquest.net", instead of needing to execute `virustotal inquest.net` you could also run `virustotal 1` and you would receive the same results. In fact, this works against any module or command that uses an artiface name as it's first argument.

Sessions are here for easy access to artifacts and will be cleared each time you quit the command line session.
If you wish to clear the session early, run the command "wipe" and you'll get a clean slate.

Eventually, we would like to add a **Cases** portion to Omnibus that allows users to create cases of artifacts, move between them, and maintain a more coherent OSINT management platform. Though for this current pre-release, we will be sticking with the Session. :)

**Interacting with Session IDs instead of Artifact names**
![Alt text](docs/images/artifact_id.png?raw=true "Shell")


### Modules
Omnibus currently supports the following list of modules. If you have suggestions or modules or would like to write one
of your own, please create a pull request.

Also, within the Omnibus console, typing the module name will show you the Help information associated with that module.

**Modules**
- Blockchain.info
- Censys
- ClearBit
- Cymon
- DNS subdomain enumeration
- DNS resolution
- DShield (SANS ISC)
* GeoIP lookup
- Full Contact
* Gist Scraping
* GitHub user search
* HackedEmails.com email search
* Hurricane Electric host search
* HIBP search
* Hunter.io
* IPInfo
* IPVoid
* KeyBase
* Nmap
* PassiveTotal
* Pastebin
* PGP Email and Name lookup
* RSS Feed Reader
* Shodan
* Security News Reader
* ThreatCrowd
* ThreatExpert
* TotalHash
* Twitter
* URLVoid
* VirusTotal
* Web Recon
* WHOIS

As these modules are a work in progress, some may not yet work as expected but this will change over the coming weeks as we hope to officially release version 1.0 to the world!

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

### Monitoring Modules
Omnibus will soon be offering the ability to monitor specific keywords and regex patterns across different sources. Once a match is found, an email or text message alert could be sent to the user to inform them on the discovery.
This could be leveraged for real-time threat tracking, identifying when threat actors appear on new forums or make a fresh Pastebin post, or simply to stay on top of the current news.

Coming monitors include:
- RSS monitor
- Pastebin monitor
- Generic Pastesite monitoring
- Generic HTTP/JSON monitoring
