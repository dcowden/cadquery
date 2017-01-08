from cadquery.impl_base.shapes import *

from OCC.BRepGProp import 
"""
    Backend must implement each objects
"""
HASH_BASE=787878

class Compound(BaseCompound):
    pass

class Solid(BaseSolid):

    #
    # TODO. I'm not really loving the three levels of constructors. and objects ( Shape->BaseSolid->Solid)
    # but i guess its not all that bad. 
    # Shape is requiring the type and id properties, and setting up hash codes and all that
    # BaseXXX is enforcing what methods are available on each one.
    #
    def __init__(self, tds_solid):
        BaseSolid.__init__(self,tds_solid.HashCode(HASH_BASE))
    	self.s = tds_solid

    def volume(self):
        raise NotImplementedError("Implement this Shape Method")
        
    def area(self):
        raise NotImplementedError("Implement this Shape Method")
    #
    # Iterators
    #        
    def faces(self):
        raise NotImplementedError("Implement this Shape Method")

    def wires(self):
        raise NotImplementedError("Implement this Shape Method")

    def edges(self):
        raise NotImplementedError("Implement this Shape Method")

    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")  

class Shell(BaseShell):
    pass

class Face(BaseFace):
    pass

class Wire(BaseWire):
    pass

class Edge(BaseEdge):
    pass

class Vertex(BaseVertex):
    pass



def compute_volume(shape):
