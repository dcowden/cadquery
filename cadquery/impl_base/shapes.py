from cadquery import Shape,ShapeType

class BaseCompound(Shape):

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
        
class BaseSolid(Shape):

    def __init__(self,shape_id):
        Shape.__init__(self,shape_id,ShapeType.SOLID)

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

class BaseShell(Shape):

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

        
class BaseFace(Shape):

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
        
class BaseWire(Shape):

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

    
class BaseEdge(Shape):

    def __init__(self):
        Shape.__init__(shape_id,ShapeType.EDGE)
        
    def length(self):
        raise NotImplementedError("Implement this Shape Method")    
    
    #
    # Iterators
    #    
    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")        

    
class BaseVertex(Shape):
    def __init__(self):
        Shape.__init__(shape_id,ShapeType.VERTEX)
    pass
