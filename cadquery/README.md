
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
	
 * impl_base -- Base classes that implementations must extend
 
    * geom: base geometric contstructs, Transforms, Vectors, BoundingBox, Planes
	* exporters: export routines
	* importers: import routines
	* operations: modelling functions that actually do work
	* shapes: the list of shapes backends must implement: Face, Wire, Edge, Vertex, Solid, etc

The implementation packages generally have an implementation module correspdonding directly to each 
module in impl_base.
	
 * freecad_impl -- FreeCAD implementation classes ( these extend backend_base )
 * pythonocc_impl -- PythonOCC implementation classes ( these extend backend_base )
 
 
 Creating a Backend
 ====================
 
 init.py of a backend should load the necessary dependencies of the framework, and raise
 an error if they are not available
 

