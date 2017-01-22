import sys, logging
import traceback

"""
    the order of these imports matter,
    it is important to prevent circular dependencies between the backend
    and core functions.

    The overall order is:

    Shapes
    Core Operations
    Backends ( should only depend on the two above)
    
    Everything Else
    
"""
import os

log = logging.getLogger("cq_init")    

                 
# the import order is important.
# we need to get the base classes that the backend implementation needs,
# then we need to import the rest
from .core.config import *
from .core.shapes import *
from .core.context import *
from .core.operations import *
from .core.sketch import *
from .core.exporter import *
from .core.importer import *


try:
    #TODO: it would be nice to avoid enumerating all of the sub-modules here,
    #but from .pythonocc_impl import * does not import the objects into the
    #top-level cadquery namespace.
    #i think we could use the imp tool to do what we want here and iterate 
    #over each one
    #IMPORTANT!! order matters here. 
    from .impl.geom import *
    from .impl.shapes import *
    from .impl.operations import *
    
    log.warn("Found PythonOCC Backend")
   
except Exception as e:
    traceback.print_exc()
    raise NotImplementedError("Cannot Load CQ: no backend available. Install OCC or FreeCAD") 

from .core.geom import *  

#TODO: need to fill this out. Its a long long list!
#tricky enough, it needs to include class names that will be defined in the backends
core_classes=[]
impl_classes=[]
__all__ = core_classes + impl_classes
        
__version__ = "2.0.0"
