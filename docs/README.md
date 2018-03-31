# omnibus
The OSINT Omnibus is meant to be a simple set of Python libraries to interact with OSINT resources which can be imported
into your own Python project for custom usage or utilized through the built-in interactive command line application
omnibus-cli.py

## Installation
### Pre-requisites
1. Run `pip install -r requirements.txt` to setup required Python packages
2. The Omnibus CLI requires MongoDB for long-term storage of artifacts and their OSINT results. Visit
   https://docs.mongodb.com/manual/installation/ for details specific to your operating system.

#### MongoDB Index
The MongoDB will work best with larger datasets if you create an index for the "name" key.
To do this, launch MongoDB using the `mongo` command. If a collection for omnibus already exists, simply run
`db.omnibus.createIndex({'name': 1])`. If you haven't yet executed omnibus-cli.py, you will need to manually create the
Mongo collection first by running: `db.createCollection('omnibus')`

### Data Schema
Each artifact is stored in MongoDB using the same schema but separated into different collections depending on the
artifact type. Omnibus currently offers three separate artifacts:
- Host
    - IPv4, IPv6, FQDN
- Email
    - Email address
- Username
    - Arbitrary string

Schema:
```
{
  "name": <primary key>,
  "data": dict of OSINT results,
  "source": arbitrary string,
  "notes": list of user added notes
}
```

