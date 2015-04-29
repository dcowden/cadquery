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
import cadquery
from OCC.gp import gp_Vec

def sortWiresByBuildOrder(wireList, plane, result=[]):
    """
        Tries to determine how wires should be combined into faces.
        Assume:
            The wires make up one or more faces, which could have 'holes'
            Outer wires are listed ahead of inner wires
            there are no wires inside wires inside wires ( IE, islands -- we can deal with that later on )
            none of the wires are construction wires
        Compute:
            one or more sets of wires, with the outer wire listed first, and inner ones
        Returns, list of lists.
    """

    remainingWires = list(wireList)
    while remainingWires:
        outerWire = remainingWires.pop(0)
        group = [outerWire]
        otherWires = list(remainingWires)
        for w in otherWires:
            if plane.isWireInside(outerWire, w):
                group.append(w)
                remainingWires.remove(w)
        result.append(group)

    return result


class Vector(object):
    """
        Create a 3-dimensional vector

        :param *args: a 3-d vector, with x-y-z parts.

        you can either provide:
            * a PythonOCC vector
            * a vector ( in which case it is copied )
            * a 3-tuple
            * three float values, x, y, and z

        This vector is immutable-- all mutations return a copy!
    """

    def __init__(self, *args):
        if len(args) == 3:
            fV = gp_Vec(args[0], args[1], args[2])
        elif len(args) == 1:
            if type(args[0]) is tuple:
                #TODO: We've been given a tuple, convert to PythonOCC vector
                pass
            elif type(args[0] is gp_Vec):
                #TODO: Fix this, we've been given a PythonOCC vector
                pass
            elif type(args[0] is Vector):
                fV = args[0].wrapped
            else:
                fV = args[0]
        else:
            raise ValueError("Expected three floats, PythonOCC vector, or 3-tuple")

        self.wrapped = fV
        self.Length = fV.Magnitude()
        self.x = fV.X()
        self.y = fV.Y()
        self.z = fV.Z()

    def toTuple(self):
        return (self.x, self.y, self.z)

    #TODO: is it possible to create a dynamic proxy without all this code?
    def cross(self, v):
        return Vector(self.wrapped.cross(v.wrapped))

    def dot(self, v):
        return self.wrapped.dot(v.wrapped)

    def sub(self, v):
        return self.wrapped.sub(v.wrapped)

    def add(self, v):
        return Vector(self.wrapped.add(v.wrapped))

    def multiply(self, scale):
        """
            Return self multiplied by the provided scalar
        """
        tmp = Geom_Vector(self.wrapped)
        return Vector(tmp.multiply(scale))

    def normalize(self):
        """
            Return normalized version this vector.
        """
        tmp = Geom_Vector(self.wrapped)
        tmp.normalize()
        return Vector(tmp)

    def Center(self):
        """
        The center of myself is myself.
        Provided so that vectors, vertexes, and other shapes all support a common interface,
        when Center() is requested for all objects on the stack
        """
        return self

    def getAngle(self, v):
        return self.wrapped.getAngle(v.wrapped)

    def distanceToLine(self):
        raise NotImplementedError("Not implemented yet.")

    def projectToLine(self):
        raise NotImplementedError("Not implemented yet.")

    def distanceToPlane(self):
        raise NotImplementedError("Not implemented yet.")

    def projectToPlane(self):
        raise NotImplementedError("Not implemented yet.")

    def __hash__(self):
        return self.wrapped.__hash__()

    def __add__(self,v):
        return self.add(v)

    def __len__(self):
        return self.Length

    def __repr__(self):
        return self.wrapped.__repr__()

    def __str__(self):
        return self.wrapped.__str__()

    def __len__(self,other):
        return self.wrapped.__len__(other)

    def __lt__(self,other):
        return self.wrapped.__lt__(other)

    def __gt__(self,other):
        return self.wrapped.__gt__(other)

    def __ne__(self,other):
        return self.wrapped.__ne__(other)

    def __le__(self,other):
        return self.wrapped.__le__(other)

    def __ge__(self,other):
        return self.wrapped.__ge__(other)

    def __eq__(self,other):
        return self.wrapped.__eq__(other)