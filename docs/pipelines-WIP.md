#### Cases
In the near future Omnibus will support the concept of **Cases** to provide a more coherent OSINT management platform. Cases allow users to create collection of artifacts that are all related to a specific investigation. Each cases will be stored in the database with a case name provided by the user, a list of artifacts added to that case (pointers to the full artifact document in MongoDB), and user defined notes relevant to the case.
Users will be able to have multiple cases open at once and navigate between them for easy multi-tasking.

### Import and Export Modules
Omnibus supports a variety of Import and Export modules which allow users to ingest new artifacts and export enriched artifacts to and from arbitrary remote endpoints, including:

- Amazon SQS Queues
- HTTP REST API endpoints
- Local JSON Files
- Local Text Files
- MISP (_support planed_)

The concept here is to allow users to create full-circle pipelines that can ingest new IOCs from sources of your choosing, enrich them with Omnibus provided OSINT sources, and then optionally export the enriched artifacts to another external system.

Import and Export modules can be defined within the Omnibus configuration file. Each time omnibus-cli.py is loaded, the import sources will be checked for new entries and automatically created as their appropriate artifact within Omnibus.

After investigating and enriching these new artifacts through the use of Omnibus modules, the Export configurations can be used to send these enriched artifacts to various remote and local sources.

#### Pipelines
Pipelines can be built to provide initial collection of new artifacts from arbitrary data sources and then enrichment of those artifacts within Omnibus. One great example of this use-case is through integration with another InQuest project [ThreatIngestor](https://github.com/InQuest/https://github.com/InQuest/ThreatIngestor).

For more information on leveraging ThreatIngestor to collect IOC's, please visit the [full documentation here](https://threatingestor.readthedocs.io/en/latest/)

At a high level, ThreatIngestor can watch arbitrary data sources (Twitter, RSS feeds, SQS, Websites, and more) and extract information such as IP addresses, URLs, domains, hashes, and YARA signatures, and then send that information to other systems for analysis. 

To create a pipeline between ThreatIngestor and Omnibus, you would first configure ThreatIngestor to monitor the data sources of your choosing and then configure the [Amazon SQS operator](https://threatingestor.readthedocs.io/en/latest/plugins/operator.html#amazon-sqs) to send the collected data to an SQS queue of your choosing.

Omnibus's configuration file would then be updated within the `import` section to monitor that same SQS queue. Each time omnibus-cli.py is loaded this SQS queue would be queried to receive any new entries since it's last check. Every new entry would be created within Omnibus as an artifact appropriate to it's type. From here you can begin enriching these artifacts using Omnibus modules and machines.

If you wanted to then send these enriched artifacts to another external system, you would update the `export` section of the configuration file with the specific export module name and parameters. 

**Automated Full-Circle Pipelines**
Export modules can be configured to send user selected artifacts or entire cases of artifacts, using the `export <artifact name | case number> <export destination>` command, or be configured to send artifacts collected from a specific `import` source to a specific `export` endpoint. 

For example, if you wanted to consume IOC's from ThreatIngestors and always send them to a specific HTTP REST API endpoint you would modify the `pipeline` section of the omnibus.conf file and for both your import and export configuration entries supply the same name to the `pipeline_name` parameter.
