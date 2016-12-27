# -*- coding: utf-8 -*-
"""
    Base Geometry. 
    Backends must return these objects as a result of operations.
    Generally, the backend will add its own properties to the object
    as neeced to keep track of the underlying object(s)
    
    Note: any behaviors in this class MUST be delegated to a 
    method provided by a backend. 
    see backend_base/shapes.py
    
    Shape class instances are immutable. property values should not be updated.
    
    This package must not have any dependencies on the backend packages, since
    they depend in turn on this.
"""

class Shape(object):
    def __init(self,id, wrapped):
        self.id = id
        self.wrapped = wrapped
        
    def __hash__(self):
        return self.id
    
    def center(self):
        raise NotImplementedError("Implement this Shape Method")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return self.id == other.id 


    
