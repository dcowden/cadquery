from cadquery.impl_base.geom import *
from OCC.gp import gp_Vec,gp_Trsf,gp_Pnt

class Vector(BaseVector):
    
    def __init__(self,x,y,z):
        self.v = gp_Vec(x,y,z)
                
    def X(self):
        return self.v.X()

    def Y(self):
        return self.v.Y()

    def Z(self):
        return self.v.Z()

    def distance(self,other):
        p1 = gp_Pnt(self.v.X(), self.v.Y(), self.v.Z())
        p2 = gp_Pnt(other.v.X(), other.v.Y(), other.v.Z())
        return p1.Distance(p2)
        
    def cross(self,another_vector):
        c = self.v.Crossed(another_vector.v)
        return  Vector(c.X(),c.Y(),c.Z())
        
        
class Transformation(BaseTransformation):

    def __init__(self):
        self.m = gp_Trsf()
 
    def transform(self, vector):
        raise NotImplementedError("Please implment this Matrix Method")
        
    def multiplied(self, another_transformation):
        raise NotImplementedError("Please implment this Matrix Method")
        
    def inverted(self):
        raise NotImplementedError("Please implment this Matrix Method")

    def scaled(self, scalar):
        raise NotImplementedError("Please implment this Matrix Method")

    def translated(self,vector):
        raise NotImplementedError("Please implment this Matrix Method")
        
    def rotated_x(self, angle):
        raise NotImplementedError("Please implment this Matrix Method")
        
    def rotated_y(self, angle):
        raise NotImplementedError("Please implment this Matrix Method")

    def rotated_z(self, angle):
        raise NotImplementedError("Please implment this Matrix Method")         
        

class BoundingBox(BaseBoundingBox):
    pass
