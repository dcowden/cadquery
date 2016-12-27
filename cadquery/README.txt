
CadQuery Structure Overview

CadQuery is designed to support multiple backend CAD systems. The backend implementations
are strickly separated from the CQ code, to enable easily adding other backend systems.

Module descriptions:
=======================

 * contrib -- Third party contributions to CQ
 * core -- Core CQ code. Nothing in this module should directly reference any backend implementation classes
 * freecad_impl -- FreeCAD implementation classes ( these extend backend_base )
 * pythonocc_impl -- PythonOCC implementation classes ( these extend backend_base )
 
 
 Creating a Backend
 ====================
 
 init.py of a backend should load the necessary dependencies of the framework, and raise
 an error if they are not available
 

