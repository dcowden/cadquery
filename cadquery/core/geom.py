from cadquery import Vector,Transformation
import math

"""
    Common Geometry Constructs
    Based upon backend implementations.
    
    This is where geometry objects that are NOT implemented natively,
    but are implemented in terms of native things go

"""

class Direction(object):
    ORIGIN=Vector(0,0,0)
    X = Vector(1,0,0)
    Y = Vector(0,1,0)
    Z = Vector(0,0,1)
    XM = Vector(-1,0,0)
    YM = Vector(0,-1,0)
    ZM = Vector(0,0,-1)

class Plane(object):
    """A 2D coordinate system in space

    A 2D coordinate system in space, with the x-y axes on the plane, and a
    particular point as the origin.

    A plane allows the use of 2-d coordinates, which are later converted to
    global, 3d coordinates when the operations are complete.

    Frequently, it is not necessary to create work planes, as they can be
    created automatically from faces.
    """

    @staticmethod
    def named(stdName, origin=Direction.ORIGIN):
        """Create a predefined Plane based on the conventional names.

        :param stdName: one of (XY|YZ|ZX|XZ|YX|ZY|front|back|left|right|top|bottom)
        :type stdName: string
        :param origin: the desired origin, specified in global coordinates
        :type origin: 3-tuple of the origin of the new plane, in global coorindates.

        Available named planes are as follows. Direction references refer to
        the global directions.

        =========== ======= ======= ======
        Name        xDir    yDir    zDir
        =========== ======= ======= ======
        XY          +x      +y      +z
        YZ          +y      +z      +x
        ZX          +z      +x      +y
        XZ          +x      +z      -y
        YX          +y      +x      -z
        ZY          +z      +y      -x
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
            'XY': Plane(origin, Direction.X, Direction.Z),
            'YZ': Plane(origin, Direction.Y, Direction.X),
            'ZX': Plane(origin, Direction.Z, Direction.Y),
            'XZ': Plane(origin, Direction.X, Direction.YM),
            'YX': Plane(origin, Direction.Y, Direction.ZM),
            'ZY': Plane(origin, Direction.Z, Direction.XM),
            'front': Plane(origin, Direction.X, Direction.Z),
            'back': Plane(origin, Direction.XM, Direction.ZM),
            'left': Plane(origin, Direction.Z, Direction.XM),
            'right': Plane(origin, Direction.ZM, Direction.X),
            'top': Plane(origin, Direction.X, Direction.Y),
            'bottom': Plane(origin, Direction.X, Direction.YM)
        }

        try:
            return namedPlanes[stdName]
        except KeyError:
            raise ValueError('Supported names are {}'.format(
                namedPlanes.keys()))

    @staticmethod
    def XY(origin=Direction.ORIGIN, xDir=Direction.X):
        plane = Plane.named('XY', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def YZ(origin=Direction.ORIGIN, xDir=Direction.Y):
        plane = Plane.named('YZ', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def ZX(cls, origin=(0, 0, 0), xDir=Direction.Z):
        plane = Plane.named('ZX', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def XZ(cls, origin=(0, 0, 0), xDir=Direction.X):
        plane = Plane.named('XZ', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def YX(cls, origin=(0, 0, 0), xDir=Direction.Y):
        plane = Plane.named('YX', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def ZY(cls, origin=(0, 0, 0), xDir=Direction.Z):
        plane = Plane.named('ZY', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def front(cls, origin=(0, 0, 0), xDir=Direction.X):
        plane = Plane.named('front', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def back(cls, origin=(0, 0, 0), xDir=Direction.XM):
        plane = Plane.named('back', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def left(cls, origin=(0, 0, 0), xDir=Direction.Z):
        plane = Plane.named('left', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def right(cls, origin=(0, 0, 0), xDir=Direction.ZM):
        plane = Plane.named('right', origin)
        plane._setPlaneDir(xDir)
        return plane

    @classmethod
    def top(cls, origin=(0, 0, 0), xDir=Direction.X):
        plane = Plane.named('top', origin)
        plane._setPlaneDir(xDir)
        return plane

    @staticmethod
    def bottom(cls, origin=(0, 0, 0), xDir=Direction.X):
        plane = Plane.named('bottom', origin)
        plane._setPlaneDir(xDir)
        return plane

    def __init__(self, origin, xDir, normal):
        """Create a Plane with an arbitrary orientation

        TODO: project x and y vectors so they work even if not orthogonal
        :param origin: the origin
        :type origin: a three-tuple of the origin, in global coordinates
        :param xDir: a vector representing the xDirection.
        :type xDir: a three-tuple representing a vector, or a FreeCAD Vector
        :param normal: the normal direction for the new plane
        :type normal: a FreeCAD Vector
        :raises: ValueError if the specified xDir is not orthogonal to the provided normal.
        :return: a plane in the global space, with the xDirection of the plane in the specified direction.
        """

        if (normal.length() == 0.0):
            raise ValueError('normal should be non null')
        self.zDir = normal.normalized()

        if (xDir.length() == 0.0):
            raise ValueError('xDir should be non null')
        self._setPlaneDir(xDir)

        self.invZDir = self.zDir.multiply(-1.0)

        self.origin = origin

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = Vector(value)
        self._calcTransforms()

    def setOrigin2d(self, x, y):
        """
        Set a new origin in the plane itself

        Set a new origin in the plane itself. The plane's orientation and
        xDrection are unaffected.

        :param float x: offset in the x direction
        :param float y: offset in the y direction
        :return: void

        The new coordinates are specified in terms of the current 2-d system.
        As an example:

        p = Plane.XY()
        p.setOrigin2d(2, 2)
        p.setOrigin2d(2, 2)

        results in a plane with its origin at (x, y) = (4, 4) in global
        coordinates. Both operations were relative to local coordinates of the
        plane.
        """
        self.origin = self.toWorldCoords((x, y))


    def toLocalCoords(self, vector):
        """Project the provided coordinates onto this plane

        :param obj: an object or vector to convert
        :type vector: a vector or shape
        :return: an object of the same type, but converted to local coordinates


        Most of the time, the z-coordinate returned will be zero, because most
        operations based on a plane are all 2-d. Occasionally, though, 3-d
        points outside of the current plane are transformed. One such example is
        :py:meth:`Workplane.box`, where 3-d corners of a box are transformed to
        orient the box in space correctly.

        """
        return self.fG.multiply(vector)

    def toWorldCoords(self, tuplePoint):
        """Convert a point in local coordinates to global coordinates

        :param tuplePoint: point in local coordinates to convert.
        :type tuplePoint: a 2 or three tuple of float. The third value is taken to be zero if not supplied.
        :return: a Vector in global coordinates
        """
        if isinstance(tuplePoint, Vector):
            v = tuplePoint
        elif isinstance(tuplePoint,tuple):
            if len(tuplePoint) == 2:
                v = Vector.create(tuplePoint[0], tuplePoint[1], 0.0)
            else:
                v = Vector.create(tuplePoint[0], tuplePoint[1], tuplePoint[2])

        return self.rG.multiply(v)

    def rotated(self, rotate=(0, 0, 0)):
        """Returns a copy of this plane, rotated about the specified axes

        Since the z axis is always normal the plane, rotating around Z will
        always produce a plane that is parallel to this one.

        The origin of the workplane is unaffected by the rotation.

        Rotations are done in order x, y, z. If you need a different order,
        manually chain together multiple rotate() commands.

        :param rotate: Vector [xDegrees, yDegrees, zDegrees]
        :return: a copy of this plane rotated as requested.
        """
        rotate = Vector.create_from_tuple(rotate)

        # Convert to radians.
        rotate = rotate.multiply(math.pi / 180.0)

        # Compute rotation matrix.
        m = Transformation()
        m = m.rotated_x(rotate.x)
        m = m.rotated_y(rotate.y)
        m = m.rotated_z(rotate.z)

        # Compute the new plane.
        newXdir = m.multiply(self.xDir)
        newZdir = m.multiply(self.zDir)

        return Plane(self.origin, newXdir, newZdir)

    def _setPlaneDir(self, xDir):
        """Set the vectors parallel to the plane, i.e. xDir and yDir"""
        if (self.zDir.dot(xDir) > 1e-5):
            raise ValueError('xDir must be parralel to the plane')

        self.xDir = xDir.normalized()
        self.yDir = self.zDir.cross(self.xDir).normalized()

    def _calcTransforms(self):
        """Computes transformation matrices to convert between coordinates

        Computes transformation matrices to convert between local and global
        coordinates.
        """
        # r is the forward transformation matrix from world to local coordinates
        # ok i will be really honest, i cannot understand exactly why this works
        # something bout the order of the translation and the rotation.
        # the double-inverting is strange, and I don't understand it.
        
        row1 = ( self.xDir.x, self.xDir.y, self.xDir.z, self.origin.x)
        row2 = ( self.yDir.x, self.yDir.y, self.yDir.z, self.origin.y)
        row3 = ( self.zDir.x, self.zDir.y, self.zDir.z, self.origin.z )
        row4 = ( 0, 0, 0, 1 ) #is this right? 
       
        r = Transformation().with_values((row1,row2,row3,row4))
        #and so on.
        # Forward transform must rotate and adjust for origin.
        #(r.A11, r.A12, r.A13) = (self.xDir.x, self.xDir.y, self.xDir.z)
        #(r.A21, r.A22, r.A23) = (self.yDir.x, self.yDir.y, self.yDir.z)
        #(r.A31, r.A32, r.A33) = (self.zDir.x, self.zDir.y, self.zDir.z)

        #invR = r.inverse()
        #invR.A14 = self.origin.x
        #invR.A24 = self.origin.y
        #invR.A34 = self.origin.z

        #self.rG = invR
        #self.fG = invR.inverse()


    