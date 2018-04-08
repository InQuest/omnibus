# omnibus
The OSINT Omnibus is meant to be a simple set of Python libraries to interact with OSINT resources which can be imported
into your own Python project for custom usage or utilized through the built-in interactive command line application
omnibus-cli.py

- [Installation](#installation)
    * [Pre-requisites](#pre-requisites)
    * [MongoDB](#mongodb)
        + [Schema](#schema)
- [Modules](#modules)
- [Use as Library](#library)
- [Interactive CLI](#interactive-cli)
    * [Configuration](#configuration)
    * [Artifacts](#artifacts)
    * [Sessions](#sessions)
    * [Reports](#reports)


## Installation
### Pre-requisites
1. Run `pip install -r requirements.txt` to setup required Python packages
2. The Omnibus CLI requires MongoDB for long-term storage of artifacts and their OSINT results. Visit
   https://docs.mongodb.com/manual/installation/ for details specific to your operating system.

### MongoDB
The MongoDB will work best with larger datasets if you create an index for the "name" key.
To create an index after your first run, launch MongoDB using your local "mongo" application and run:
`db.omnibus.createIndex({'name': 1])`. 

#### Schema
Each item you investigate is called an "artifact" within the Omnibus suite. Every artifact you create within the CLI is
stored in MongoDB using the following schema:

```
{
  "name": artifact name (e.g., hostname, ip address, username, email address, bitcoin address, hash),
  "data": dictionary of module results,
  "source": user-defined string to track where the artifact came from,
  "notes": list of user-defined notes
}
```
Omnibus currently supports the following artifact types:
- Host
    - IPv4, IPv6, FQDN
- Email Address
- User Name
- Hash
    - MD5, SHA1, SHA256, SHA512
- Bitcoin Address

**Note:** For more detailed information of artifacts, please read the [Artifacts](#Artifacts) section of this document.

When modules are executed Omnibus will first check MongoDB to see if there's a document for the artifact. If so, the
results for the executed module will be added to the document under the `data` key as a dictionary where the module name
is the new key. When modules are re-executed against an artifact with an existing entry for that module, the old data
will be overwritten with the new.

### Modules
Omnibus currently supports the following list of modules. If you have suggestions or modules or would like to write one
of your own, please create a pull request.

- Blockchain.info
- Censys
- ClearBit
- Cymon
- DNS resolution
- DShield (SANS ISC)
- Full Contact
- Geolocation
- Gist search
- GitHub username lookup
- GitLab username lookup
- HackedEmails.com
- HaveIBeenPwned.com
- IPVoid
- Keybase username lookup
- Malcode
- Malware Domain List
- NMap scanner
- PassiveTotal
- PhishTank
- Project Honeypot
- Reddit username lookup
- RSS reader (with keyword monitoring and text message notifications)
- SANS ISC
- Security News reader (Google News)
- Shodan
- Twitter
- URLVoid
- Usersearch.com
- VirusTotal
- Webserver fingerprinting
- WHOIS

### Library
To utilize the Omnibus modules within your own Python projects, first install the library to your system:
1. `git clone https://github.com/deadbits/omnibus`
2. `cd omnibus && python setup.py install`
3. `mkdir /opt/omnibus`

The /opt/omnibus folder will be where your API keys are held. Copy the `omnibus/etc/apikeys.json` file into this folder
and add each API key you have to the designated keys.

### Interactive CLI
The omnibus-cli.py script provides an interactive command line for you to add and track multiple artifacts, execute
modules against MongoDB- stored artifacts or one-off artifacts you don't wish to store, add notes and sources to
artifacts, and much more.

The command line script attempts to mimic some common Linux console commands for ease of use. Omnibus provides commands
such as `cat` to show information about an artifact, `rm` to remove an artifact from the database, `ls` to view
currently cached artifacts, and so on.

Start the CLI by simply executing `omnibus-cli.py` and ensure the "etc/apikeys.json" file has all your required keys
saved.

Within the CLI you can get a list of all commands by using the "help" command. For each individual command, typing
"help" and the name of the command will print the help information for that specific command.

Some quick commands to remember are:
- `session` - start a new artifact cache
- `cat <artifact name>|apikeys` - pretty-print an artifacts document or view your stored API keys
- `open <file path>` - load a text file list of artifacts into Omnibus for investigation
- `new <artifact name>` - create a new artifact and add it to MongoDB and your session
- `find <artifact name>` - check if an artifact exists in the db and show the results
- `ls` - view all artifacts in your session
- `wipe` - clear your current session
- `modules` - show a list of all available modules


#### Configuration
Setting up the CLI application is very straight forward and only requires that you add any API keys you have to the
"etc/apikeys.json" file. Within this file there is a key for each service that requires an API key. Add your keys as the
values and save the file. Good to go.

For more granular control over the application, you can edit the "etc/omnibus.conf" file. This file allows you to
configure command line history, SOCKS proxy settings, reports directory and format,  and MongoDB/Redis options.

#### Artifacts
Within the Omnibus command line, items to investigate are created as "Artifacts". Artifacts can be one of the following:
- Host (IPv4, IPv6, FQDN)
- Email Address
- Username
- Hash (MD5, SHA1, SHA256, SHA512)
- Bitcoin Address

To create a new artifact and add it to MongoDB for tracking, run the command `new <artifact name>`. For example, to
start investigation the domain deadbits.org, you would run `new deadbits.org`.

Omnibus automatically determines which type of artifact you created, adds it to the correct MongoDB collection with the
schema discussed above, and adds a pointer of that artifact to the Session Cache.

#### Sessions
Omnibus sessions provide a quick and easy way to investigate multiple hosts without having to manually keep track of all
the artifacts you are tracking or having to re-type the artifact name for every module execution.

This is done by using either a Redis based cache or a pure Python list based cache.

After starting omnibus-cli.py, create a new session with the `session` command. This will create a new in-memory cache
to track your artifacts. Please note you do not need to start a session within the CLI, it is just an added feature for
ease of use - not every item from MongoDB will always be in the session cache.

Artifacts are added to the session cache as a dictionary with an integer as the key and the artifact name as the value.
For example, the first artifact (e.g., deadbits.org) would have a key of "1" and a value of deadbits.org. The second
artifact added will have a key of "2" and so on.

After an artifact is added to the session, you can interact with it by simply providing the key instead of typing the
entire name. Still using the "deadbits.org" artifact, to get the WHOIS records you would simply run `whois 1`. This is
the same as running `whois deadbits.org`.

Sessions are also how you can add a source to your artifact or add notes. Once an artifact is added, you can use the
"source" and "notes" command to update those values in MongoDB. By default these commands will update the most recently
added artifact, but you can specify an artifact ID as the second argument of each command.

**Source:**
This is meant as a quick way to track where a piece of information came from. The source value can be any arbitrary
string you'd like such as a URL, individuals name, blog title, etc.

Commands:
- source view <session id|artifact name>
- source add <session id|artifact name> <source>

**Notes:**
Notes can be used to keep track of additional information that didn't come from a module. Just like source, notes can be
anything you want.

Commands:
- notes view <session id|artifact name>
- notes add <session id|artifact name> <note>
- notes rm <session id|artifact name> <list index of note to remove>

#### Reports
Using the "report" command will create either an HTML formatted or JSON formatted file with all of the database stored
information of an artifact. By default Omnibus will save these into the "reports" folder at the top level directory but
you can specify any path you wish.

In addition, any module or command can have it's output saved to a local file by using the ">" redirector. For example,
to save the JSON output of an Nmap scan against deadbits.org you would run `nmap deadbits.org > ~/Desktop/results.json`.
As expected this will save the pretty-printed JSON results to ~/Desktop/results.json.

To create a report of all artifact information, instead of a single modules output, you can use the "report" command
detailed below.

**Commands:**
- report html <artifact name>
- report json <artifact name>
