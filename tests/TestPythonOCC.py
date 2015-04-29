#import unittest
#from tests import BaseTest

import sys
sys.path.insert(0, '/home/jwright/Downloads/cadquery/')

from cadquery.pythonocc_impl.geom import Vector
from OCC.Geom import Geom_Vector

class TestPythonOCC():
    def testVectorConstructors(self):
        v1 = Vector(1, 2, 3)
        v2 = Vector((1, 2, 3))
        v3 = Vector(Geom_Vector(1, 2, 3))
        v4 = Vector(Vector(1, 2, 3))

        for v in [v1, v2, v3, v4]:
            self.assertTupleAlmostEquals((1, 2, 3), v.toTuple(), 4)

def main():
    TestPythonOCC().testVectorConstructors()

if __name__ == "__main__":
    main()