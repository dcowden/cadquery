"""
    Copyright (C) 2011-2015  Parametric Products Intellectual Holdings, LLC

    This file is part of CadQuery.

    CadQuery is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    CadQuery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; If not, see <http://www.gnu.org/licenses/>
"""

import math
from cadquery.impl_base.geom import *
import FreeCAD
import Part as FreeCADPart



class Vector(BaseVector):
    """Create a 3-dimensional vector

        :param args: a 3-d vector, with x-y-z parts.

        you can either provide:
            * nothing (in which case the null vector is return)
            * a FreeCAD vector
            * a vector ( in which case it is copied )
            * a 3-tuple
            * three float values, x, y, and z
    """
    def __init__(self, x,y,z):
        self.fV = FreeCAD.Base.Vector(x, y, z)

    def X(self):
        return self.fV.x

    def Y(self):
        return self.fV.y

    def Z(self):
        return self.fV.z

    def Length(self):
        return self.fV.Length

    def distance(self,other):
        return self.fV.distanceToPoint(other.fV)
        
    # TODO: is it possible to create a dynamic proxy without all this code?
    def cross(self, v):
        return Vector(self.fV.cross(v.fV))

    def dot(self, v):
        return self.fV.dot(v.fV)

    def sub(self, v):
        return Vector(self.fV.sub(v.fV))

    def add(self, v):
        return Vector(self.fV.add(v.fV))

    def multiply(self, scale):
        """Return a copy multiplied by the provided scalar"""
        tmp_fc_vector = FreeCAD.Base.Vector(self.fV)
        return Vector(tmp_fc_vector.multiply(scale))

    def normalized(self):
        """Return a normalized version of this vector"""
        tmp_fc_vector = FreeCAD.Base.Vector(self.fV)
        tmp_fc_vector.normalize()
        return Vector(tmp_fc_vector)

    def getAngle(self, v):
        return self.fV.getAngle(v.fV)



class Transformation(BaseTransformation):
    """
        PARTIAL IMPLEMENTAtION ONLY!
    """
    def __init__(self):
        self.m = FreeCAD.Base.Matrix()

    def rotated_x(self, angle):
        self.m.rotateX(angle)

    def rotated_y(self, angle):
        self.m.rotateY(angle)


class BoundingBox(BaseBoundingBox):
    pass


