# Contributing
Omnibus is designed to easily support the addition of new modules with very few requirements.
The omnibus-cli.py script passes arguments and their designed calling module name to the Dispatch class.
Dispatch handles verifying that the artifact is a valid type for the module and execution of the module if this check
passes.

## Custom Modules
Each module must include the following:
- Function named "main" that accepts two parameters only; "artifact" and "artifact_type"
    - "main" is the primary function of your module, called by Dispatch.submit. This function should simply call other
        functions in your module that perform the real work. Must return final results as JSON or Python dictionary
    - "artifact" is the string name of the artifact the module is executing against. For example, "deadbits.org" is an
        artifact or "50.116.59.164".
    - "artifact_type" is determined by the pre-processing done in Dispatch.submit. This will be a string that identifies
        the artifact to be processed, such as "ipv4", "fqdn", "hash", etc. You can check this variable within your
        function if your module can run on different artifact types but performs a different task depending on the type
        - for an example of this, see the virustotal.py module
- Function named or suffixed with "run"
    - This function, or functions, should perform the real work of your module and get called by "main"
    - Common tasks: Perform HTTP request to OSINT source to lookup artifact, returns JSON result

The libraries "common.py" and "http.py" provide several commonly used methods that you may leverage when creating a
module. To access these you can simply add an import statement at the top of your module; e.g., `from common import
is_ipv4` or `from http import get`.


**Boilerplate module with empty functions**
```
def fqdn_run(artifact_name):
    # run this func if artifact is a domain
    pass

def ip_run(artifact_name):
    # run this func if artifact is ipv4 address
    pass


def main(artifact, artifact_type):
    # Dispatch.run calls this function
    if artifact_type == 'ipv4':
        result = ip_run(artifact)
    elif artifact_type == 'fqdn':
        result = fqdn_run(artifact)

    return result
```

## Command Line Support
Once a module is created, in order to provide command line support for your module you must add an associated
`do_<module name>` function to `omnibus-cli.py`. Below is an example of the do_ function for a module named "urlvoid".
Following this example, there must be a file within lib/modules called "urlvoid.py".

```
    def do_urlvoid(self, arg):
        """Search URLVoid for domain name"""
        self.dispatch.submit(self.session, 'urlvoid', arg)
```

The dispatch.submit() function takes `self.session` as it's first argument, the name of your module as it's second, and
the input argument/artifact as the third and final.
