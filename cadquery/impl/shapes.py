from cadquery import Shape,ShapeType


HASH_BASE=787878

class Compound(Shape):

    def __init__(self,compound_id):
        Shape.__init__(shape_id,ShapeType.COMPOUND)
        
    def volume(self):
        raise NotImplementedError("Implement this Shape Method")
        
    def area(self):
        raise NotImplementedError("Implement this Shape Method")
        
    #
    # Iterators
    #
    def solids(self):
        raise NotImplementedError("Implement this Shape Method")
        
    def faces(self):
        raise NotImplementedError("Implement this Shape Method")

    def wires(self):
        raise NotImplementedError("Implement this Shape Method")
        
    def edges(self):
        raise NotImplementedError("Implement this Shape Method")

    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")        
        
class Solid(Shape):
        
    def __init__(self, tds_solid):
        shape_id = tds_solid.HashCode(HASH_BASE)
        Shape.__init__(self,shape_id,ShapeType.SOLID)
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

class Shell(Shape):

    def __init__(self,shell_id):
        Shape.__init__(shape_id,ShapeType.SHELL)
        
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

        
class Face(Shape):

    def __init__(self):
        Shape.__init__(shape_id,ShapeType.FACE)
        
    def area(self):
        raise NotImplementedError("Implement this Shape Method")    
    #
    # Iterators
    #    
    def wires(self):
        raise NotImplementedError("Implement this Shape Method")
    
    def edges(self):
        raise NotImplementedError("Implement this Shape Method")

    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")        
        
class Wire(Shape):

    def __init__(self):
        Shape.__init__(shape_id,ShapeType.WIRE)
        
    def length(self):
        raise NotImplementedError("Implement this Shape Method")    
    #
    # Iterators
    #    
    def edges(self):
        raise NotImplementedError("Implement this Shape Method")

    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")        

    
class Edge(Shape):

    def __init__(self):
        Shape.__init__(shape_id,ShapeType.EDGE)
        
    def length(self):
        raise NotImplementedError("Implement this Shape Method")    
    
    #
    # Iterators
    #    
    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")        

    
class Vertex(Shape):
    def __init__(self):
        Shape.__init__(shape_id,ShapeType.VERTEX)
    pass
