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

CQ_BACKEND_ENV_VAR="CQ_BACKEND"

class CQ_Backends:
    PYTHONOCC="pythonOCC"
    FREECAD="FreeCAD"

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


#python is really weird with loading modules.
#id really like to clean up this code, but alas, you cannot use
#from <> import * from within a function, unless we get into using importlib
user_supplied_choice = os.environ.get(CQ_BACKEND_ENV_VAR)

try_loading_freecad=False
try_loading_pythonocc=False
backend_loaded = False


def equals_ignore_case(string1, string2):
    if string1 is not None and string2 is not None:
        return string1.lower() == string2.lower()
    if string1 is None and string2 is None:
        return True
    else:
        return False
        
if user_supplied_choice:
    
    if equals_ignore_case(user_supplied_choice ,CQ_Backends.PYTHONOCC):
        log.info("PythonOCC Backend Selected")
        try_loading_pythonocc=True
    
    elif equals_ignore_case(user_supplied_choice, CQ_Backends.FREECAD):
        log.info("FreeCAD Backend Selected")
        try_loading_freecad=True

    else:
        raise NotImplementedError("Unknown Backend '%s'" % user_supplied_choice)
else:
    log.info("No CQ Backend Selected. Trying all Backends available")
    try_loading_freecad=True
    try_loading_pythonocc=True
    
    
#try OCC First
if try_loading_pythonocc and ( not backend_loaded) :
    try:
        #TODO: it would be nice to avoid enumerating all of the sub-modules here,
        #but from .pythonocc_impl import * does not import the objects into the
        #top-level cadquery namespace.
        #i think we could use the imp tool to do what we want here and iterate 
        #over each one
        #IMPORTANT!! order matters here. 
        from .pythonocc_impl.geom import *
        from .pythonocc_impl.shapes import *
        from .pythonocc_impl.operations import *
        
        log.warn("Found PythonOCC Backend")
        backend_loaded = True
       
    except Exception as e:
        traceback.print_exc()
        log.warn("Exception loading PythonOCC backend",e )  
    
#Then FreeCAD
if try_loading_freecad and ( not backend_loaded) :
    try:
        from .freecad_impl.geom import *
        from .freecad_impl.operations import *
        from .freecad_impl.shapes import *
        log.warn("Found FreeCAD Backend")
        backend_loaded = True
    except Exception as e:
        traceback.print_exc()
        log.warn("Exception loading FreeCAD backend",e )          

if not backend_loaded:
    raise NotImplementedError("Cannot Load CQ: no backend available. Install OCC or FreeCAD")
    
from .core.geom import *
from .core.selectors import *
from .core.cq import *
from .core.cqgi import *      

#TODO: need to fill this out. Its a long long list!
#tricky enough, it needs to include class names that will be defined in the backends
core_classes=[]
impl_classes=[]
__all__ = core_classes + impl_classes
        
__version__ = "2.0.0"
