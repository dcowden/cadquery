
CadQuery Structure Overview

CadQuery is designed to support multiple backend CAD systems. The backend implementations
are strickly separated from the CQ code, to enable easily adding other backend systems.

Module descriptions:
=======================

 * contrib -- Third party contributions to CQ
 * core -- Core CQ code. Nothing in this module should directly reference any backend implementation classes
 
    * config : configuration objects
	* context: CQ top level classes that tie evertything in the fluent api together
	* cq: The fluent api
	* cqgi: interface for building CQ models from inside other containers
	* exporter: export routines
	* geom: core geometry classes like directions, planes, etc
	* importer: import routines
	* operations: base classes for modellig operations and their results
	* selectors: cq selectors
	* shapes: base shape object definitions 
 * impl -- python OCC implementation
 
Thoughts On How Things should work
=======================

 1. queries are the key to robust handling of geometry that changes
 2. users want to use variables not queries
 3. a single modeling context is a reqiurement
 4. users dont want to deal with the context
 5. the direct api needs to deal with queries and contexts-- there is no avoiding it

Questions
-----------



