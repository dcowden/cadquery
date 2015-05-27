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
from OCC.gp import gp_Vec, gp_Trsf, gp_Mat, gp_OX, gp_OY

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

        v0 = self.wrapped.Crossed(v.wrapped)
        return Vector(v0)

    def dot(self, v):
        """
        Return the dot product of self and v
        :param v: The vector to take the dot product of with self
        :return: A scalar representing the dot product of self and v
        """

        dP = self.wrapped.Dot(v.wrapped)
        return dP

    def sub(self, v):
        """
        Return the provided vector subtracted from self
        :param v: The Vector to subtract from self
        :return: A new Vector object that is the subtracted product of self and v
        """

        v0 = self.wrapped.Subtracted(v.wrapped)
        return Vector(v0)

    def add(self, v):
        """
        Return self added to the provided vector
        :param v: The Vector to add to self
        :return: A new Vector object that is the added product of self and v
        """

        v0 = self.wrapped.Added(v.wrapped)
        return Vector(v0)

    def multiply(self, scale):
        """
        Return self multiplied by the provided scalar
        :param scale: The scalar to multiply this Vector by
        :return: A new Vector object that is this Vector multiplied by the scalar
        """

        v0 = self.wrapped.Multiplied(scale)
        return Vector(v0)

    def normalize(self):
        """
        Return normalized version this vector
        :return: A new Vector object that is a normalized copy of this Vector
        """

        v0 = self.wrapped.Normalized()
        return Vector(v0)

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

        angle = self.wrapped.Angle(v.wrapped)
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

class Plane:
    """
    A 2d coordinate system in space, with the X-Y axes on the a plane, and a particular point as the origin.

    A plane allows the use of 2d coordinates, which are later converted to global, 3d coordinates when
    the operations are complete.

    Frequently, it is not necessary to create work planes, as they can be created automatically from faces.
    """

    def __init__(self, origin, xDir, normal):
        """
        Create a Plane with an arbitrary orientation

        TODO: project x and y vectors so they work even if not orthogonal
        :param origin: the origin
        :type origin: a three-tuple of the origin, in global coordinates
        :param xDir: a vector representing the xDirection.
        :type xDir: a three-tuple representing a Vector, or a PythonOCC Vector
        :param normal: the normal direction for the new plane
        :type normal: a Vector
        :raises: ValueError if the specified xDir is not orthogonal to the provided normal.
        :return: a plane in the global space, with the xDirection of the plane in the specified direction.
        """

        # Support tuples instead of forcing the use of vectors
        if type(origin) is tuple:
            origin = Vector(origin)
        if type(xDir) is tuple:
            xDir = Vector(xDir)
        if type(normal) is tuple:
            normal = Vector(normal)

        self.xDir = xDir.normalize()
        self.yDir = normal.cross(self.xDir).normalize()
        self.zDir = normal.normalize()

        self.invZDir = self.zDir.multiply(-1.0)

        self.setOrigin3d(origin)

    @classmethod
    def named(cls, stdName, origin=(0, 0, 0)):
        """
        Create a predefined Plane based on the conventional names.

        :param stdName: one of (XY|YZ|XZ|front|back|left|right|top|bottom
        :type stdName: string
        :param origin: the desired origin, specified in global coordinates
        :type origin: 3-tuple of the origin of the new plane, in global coordinates.

        Available named planes are as follows. Direction references refer to the global
        directions

        =========== ======= ======= ======
        Name        xDir    yDir    zDir
        =========== ======= ======= ======
        XY          +x      +y      +z
        YZ          +y      +z      +x
        XZ          +x      +z      -y
        front       +x      +y      +z
        back        -x      +y      -z
        left        +z      +y      -x
        right       -z      +y      +x
        top         +x      -z      +y
        bottom      +x      +z      -y
        =========== ======= ======= ======
        """

        namedPlanes = {
            # origin, xDir, normal
            'XY': Plane(Vector(origin), Vector((1, 0, 0)), Vector((0, 0, 1))),
            'YZ': Plane(Vector(origin), Vector((0, 1, 0)), Vector((1, 0, 0))),
            'XZ': Plane(Vector(origin), Vector((1, 0, 0)), Vector((0, -1, 0))),
            'front': Plane(Vector(origin), Vector((1, 0, 0)), Vector((0, 0, 1))),
            'back': Plane(Vector(origin), Vector((-1, 0, 0)), Vector((0, 0, -1))),
            'left': Plane(Vector(origin), Vector((0, 0, 1)), Vector((-1, 0, 0))),
            'right': Plane(Vector(origin), Vector((0, 0, -1)), Vector((1, 0, 0))),
            'top': Plane(Vector(origin), Vector((1, 0, 0)), Vector((0, 1, 0))),
            'bottom': Plane(Vector(origin), Vector((1, 0, 0)), Vector((0, -1, 0)))
        }

        if stdName in namedPlanes:
            return namedPlanes[stdName]
        else:
            raise ValueError("Supported names are %s " % str(namedPlanes.keys()))

    @classmethod
    def XY(cls, origin=(0, 0, 0)):
        return Plane.named('XY', origin)

    @classmethod
    def YZ(cls, origin=(0, 0, 0)):
        return Plane.named('YZ', origin)

    @classmethod
    def XZ(cls, origin=(0, 0, 0)):
        return Plane.named('XZ', origin)

    @classmethod
    def front(cls, origin=(0, 0, 0)):
        return Plane.named('front', origin)

    @classmethod
    def back(cls, origin=(0, 0, 0)):
        return Plane.named('back', origin)

    @classmethod
    def left(cls, origin=(0, 0, 0)):
        return Plane.named('left', origin)

    @classmethod
    def right(cls, origin=(0, 0, 0)):
        return Plane.named('right', origin)

    @classmethod
    def top(cls, origin=(0, 0, 0)):
        return Plane.named('top', origin)

    @classmethod
    def bottom(cls, origin=(0, 0, 0)):
        return Plane.named('bottom', origin)

    def setOrigin3d(self, originVector):
        """
        Move the origin of the plane, leaving its orientation and xDirection unchanged.
        :param originVector: the new center of the plane, *global* coordinates
        :type originVector: a Vector
        :return: void
        """

        # Support tuples that are used as Vectors
        if type(originVector) is tuple:
            originVector = Vector(originVector)

        self.origin = originVector
        # self._calcTransforms()

    def setOrigin2d(self, x, y):
        """
            Set a new origin based off the plane. The plane's orientation and x direction are unaffected.

            :param float x: offset in the x direction
            :param float y: offset in the y direction
            :return: void

            The new coordinates are specified in terms of the current 2-d system. As an example:
                p = Plane.XY()
                p.setOrigin2d(2,2)
                p.setOrigin2d(2,2)

            results in a plane with its origin at (x,y)=(4,4) in global coordinates. The both operations were relative
            to the local coordinates of the plane.

        """
        self.setOrigin3d(self.toWorldCoords((x, y)))

    def toLocalCoords(self, obj):
        """
            Project the provided coordinates onto this plane.

            :param obj: an object or vector to convert
            :type vector: a vector or shape
            :return: an object of the same type as the input, but converted to local coordinates


            Most of the time, the z-coordinate returned will be zero, because most operations
            based on a plane are all 2-d. Occasionally, though, 3-d points outside of the current plane are transformed.
            One such example is :py:meth:`Workplane.box`, where 3-d corners of a box are transformed to orient the box
            in space correctly.
        """
        if isinstance(obj, Vector):
            # TODO: Rework this to work with PythonOCC instead of the complicated FreeCAD way
            # return Vector(self.fG.multiply(obj.wrapped))
            pass
        elif isinstance(obj, cadquery.Shape):
            # TODO: Rework this
            # return obj.transformShape(self.rG)
            pass
        else:
            raise ValueError("Dont know how to convert type %s to local coordinates" % str(type(obj)))

    # def _calcTransforms(self):
    #     """
    #     Computes transformation matrices to convert between local and global coordinates
    #     """
    #
    #     # r is the forward transformation matrix from world to local coordinates
    #     r = gp_Mat()
    #
    #     # Forward transform must rotate and adjust for origin
    #     r.SetValue(1, 1, self.xDir.x)  # A11
    #     r.SetValue(1, 2, self.xDir.y)  # A12
    #     r.SetValue(1, 3, self.xDir.z)  # A13
    #     r.SetValue(2, 1, self.yDir.x)  # A21
    #     r.SetValue(2, 2, self.yDir.y)  # A22
    #     r.SetValue(2, 3, self.yDir.z)  # A23
    #     r.SetValue(3, 1, self.zDir.x)  # A31
    #     r.SetValue(3, 2, self.zDir.y)  # A32
    #     r.SetValue(3, 3, self.zDir.z)  # A33
    #
    #     invR = r.Inverted()
    #
    #     # TODO: gp_Mat doesn't support 4 dimensions, figure out what to do
    #     # invR.SetValue(1, 4, self.origin.x)  # A14
    #     # invR.SetValue(2, 4, self.origin.y)  # A24
    #     # invR.SetValue(3, 4, self.origin.z)  # A34
    #
    #     # (invR.A14, invR.A24, invR.A34) = (self.origin.x, self.origin.y, self.origin.z)
    #
    #     # TODO: This double inversion may not be needed with PythonOCC, find out
    #     (self.rG, self.fG) = (invR, invR.Inverted())
