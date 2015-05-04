import unittest

import sys
sys.path.insert(0, '/home/jwright/Downloads/cadquery/')

from cadquery.pythonocc_impl.geom import Vector
from OCC.gp import gp_Vec

class TestPythonOCC(unittest.TestCase):
    #TODO: Take this out and use the one in tests/__init__.py
    def assertTupleAlmostEquals(self, expected, actual, places):
        for i, j in zip(actual, expected):
            self.assertAlmostEquals(i, j, places)

    def testVectorConstructors(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector((1, 2, 3))
        v3 = Vector(gp_Vec(1, 2, 3))
        v4 = Vector(Vector(1, 2, 3))

        for v in [v1, v2, v3, v4]:
            self.assertEquals((1, 2, 3), v.toTuple(), 4)

    def testVectorLength(self):
        v1 = Vector(1, 2, 3)

        self.assertAlmostEquals(v1.Length, 3.74165738677)

    def testVectorCross(self):
        v1 = Vector(3, -3, 1)
        v2 = Vector(4, 9, 2)

        v3 = v1.cross(v2)

        self.assertEquals((-15.0, -2.0, 39.0), v3.toTuple())

    def testVectorDot(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(4, -5, 6)

        dP = v1.dot(v2)

        self.assertEquals(dP, 12)

    def testVectorSubtract(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(3, 2, 1)

        v3 = v1.sub(v2)

        self.assertEquals((-2, 0, 2), v3.toTuple())

    def testVectorAdd(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(3, 2, 1)

        v3 = v1.add(v2)

        self.assertEquals((4, 4, 4), v3.toTuple())

    def testVectorMultiply(self):
        v1 = Vector(1, 2, 3)
        scale = 2.0

        v2 = v1.multiply(scale)

        self.assertEquals((2, 4, 6), v2.toTuple())

    def testVectorNormalize(self):
        v1 = Vector(1, 2, 3)

        vN = v1.normalize()

        self.assertTupleAlmostEquals((0.267, 0.535, 0.802), vN.toTuple(), 3)

    def testVectorGetAngle(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(3, 2, 1)

        angle = v1.getAngle(v2)

        self.assertAlmostEquals(0.775, angle, 3)

    def testVectorInternals(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector(3, 2, 1)
        v3 = Vector(1, 2, 3)
        v4 = Vector(4, 5, -6)

        v1.__hash__()
        v1.__add__(v2)
        v1.__repr__()
        v1.__str__()

        # Just test that the others don't raise exceptions, but make sure these give correct values
        len = v1.__len__()
        self.assertAlmostEquals(3.742, len, 3)

        equal = v1.__eq__(v4)
        self.assertFalse(equal)
        equal = v1.__eq__(v3)
        self.assertTrue(equal)

if __name__ == '__main__':
    unittest.main()
