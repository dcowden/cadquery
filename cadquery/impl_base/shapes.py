from cadquery import Shape

class BaseCompound(Shape):

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

    def length(self):
        raise NotImplementedError("Implement this Shape Method")    
    
    #
    # Iterators
    #    
    def vertices(self):
        raise NotImplementedError("Implement this Shape Method")        

    
class BaseVertex(Shape):
    pass
