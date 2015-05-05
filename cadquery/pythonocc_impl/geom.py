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
from OCC.gp import gp_Vec, gp_Trsf, gp_OX, gp_OY

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
        if len(args) == 3:  # 3 float values
            fV = gp_Vec(args[0], args[1], args[2])
        elif len(args) == 1:
            if type(args[0]) is tuple:  # 3-tuple
                fV = gp_Vec(args[0][0], args[0][1], args[0][2])
            elif type(args[0]) is gp_Vec:  # PythonOCC vector
                fV = args[0]
            elif type(args[0]) is Vector:  # A CQ vector
                fV = args[0].wrapped
            else:
                raise ValueError("Expected three floats, PythonOCC vector, Vector, or 3-tuple")
        else:
            raise ValueError("Expected three floats, PythonOCC vector, Vector, or 3-tuple")

        self.wrapped = fV
        self.Length = fV.Magnitude()
        self.x = fV.X()
        self.y = fV.Y()
        self.z = fV.Z()

    def copy(self):
        """
        Returns a copy of this vector to avoid mutations
        :return: A new vector with the same X, Y, and Z values as this Vector
        """
        return Vector(self.x, self.y, self.z)

    def toTuple(self):
        """
        Collect the X, Y, and Z values of this vector into a tuple
        :return: A tuple representing the X, Y, and Z of this Vector
        """
        return (self.x, self.y, self.z)

    #TODO: is it possible to create a dynamic proxy without all this code?
    def cross(self, v):
        """
        Return the cross product of self and v
        :param v: The vector to take the cross product of with self
        :return: A Vector representing the cross product of self and v
        """
        v0 = self.copy()

        # Cross returns none, so we have to let it modify the v0 vector
        v0.wrapped.Cross(v.wrapped)

        return Vector(v0.wrapped)

    def dot(self, v):
        """
        Return the dot product of self and v
        :param v: The vector to take the dot product of with self
        :return: A scalar representing the dot product of self and v
        """
        v0 = self.copy()

        dP = v0.wrapped.Dot(v.wrapped)

        return dP

    def sub(self, v):
        """
        Return the provided vector subtracted from self
        :param v: The Vector to subtract from self
        :return: A new Vector object that is the subtracted product of self and v
        """
        v0 = self.copy()

        v0.wrapped.Subtract(v.wrapped)

        return Vector(v0.wrapped)

    def add(self, v):
        """
        Return self added to the provided vector
        :param v: The Vector to add to self
        :return: A new Vector object that is the added product of self and v
        """
        v0 = self.copy()

        v0.wrapped.Add(v.wrapped)

        return Vector(v0.wrapped)

    def multiply(self, scale):
        """
        Return self multiplied by the provided scalar
        :param scale: The scalar to multiply this Vector by
        :return: A new Vector object that is this Vector multiplied by the scalar
        """
        v0 = self.copy()

        v0.wrapped.Multiply(scale)

        return Vector(v0.wrapped)

    def normalize(self):
        """
        Return normalized version this vector
        :return: A new Vector object that is a normalized copy of this Vector
        """
        v0 = self.copy()

        v0.wrapped.Normalize()

        return Vector(v0.wrapped)

    def Center(self):
        """
        The center of myself is myself.
        Provided so that vectors, vertexes, and other shapes all support a common interface,
        when Center() is requested for all objects on the stack
        """
        return self

    def getAngle(self, v):
        """
        Returns the angle between the two vectors self and v
        :param v: The other vector to use with self to find the angle
        :return:
        """
        v0 = self.copy()

        angle = v0.wrapped.Angle(v.wrapped)

        return angle

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

    def __add__(self, v):
        return self.add(v)

    def __len__(self):
        return self.Length

    def __repr__(self):
        return self.wrapped.__repr__()

    def __str__(self):
        return self.wrapped.__str__()

    def __eq__(self, other):
        return self.wrapped.IsEqual(other.wrapped, 3, 3)

    # TODO: Not sure of the meaning or usefulness of this
    # def __len__(self, other):
    #     return self.wrapped.__len__(other)

    def __lt__(self, other):
        raise NotImplementedError("Not implemented yet.")

    def __gt__(self, other):
        raise NotImplementedError("Not implemented yet.")

    def __ne__(self, other):
        raise NotImplementedError("Not implemented yet.")

    def __le__(self, other):
        raise NotImplementedError("Not implemented yet.")

    def __ge__(self, other):
        raise NotImplementedError("Not implemented yet.")

class Matrix:
    """
    A 3D transformation matrix used to move geometry in space.
    """
    def __init__(self, matrix=None):
        if matrix is None:
            self.wrapped = gp_Trsf()
        else:
            self.wrapped = matrix

    def copy(self):
        """
        Returns a copy of this matrix to avoid mutations.
        :return: A copy with the same matrix contents
        """
        return Matrix(self.wrapped)

    def rotateX(self, angle):
        """
        Rotates the matrix around the X axis.
        :param angle: The angle of rotation in radians
        :return: A copy of this matrix rotated by the given angle
        """
        m0 = self.copy()

        m0.wrapped.SetRotation(gp_OX(), angle)

        return m0

    def rotateY(self, angle):
        """
        Rotates the matrix around the Y axis.
        :param angle: The angle of rotation in radians
        :return: A copy of this matrix rotated by the given angle
        """
        m0 = self.copy()

        m0.wrapped.SetRotation(gp_OY(), angle)

        return m0