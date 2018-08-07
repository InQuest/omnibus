.. _vocabulary:

Vocabulary
==========
Before we begin going deeper in Omnibus, we'll need to cover some terminology used by system.

* Artifact
  * An item to investigate
  * Artificats can be created in two ways:
      * Using the ``new`` command or by being discoverd through module execution
* Session
  * Cache of artifacts created after starting the Omnibus CLI
  * Each artifact in a session is given an ID to quickly identify and retrieve the artifact from the cache
  * Commands can be executed against an artifact either by providing it's name or it's corresponding session ID
* Module
  * Python script that performs some arbitirary OSINT task against an artifact
