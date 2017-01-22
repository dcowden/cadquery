
from cadquery import ShapeLog,ReferenceType,ActionType

#we need a couple of test implementations
#so that we can do some backend-independent tests
#if we use the real backedn, we'll have to create real solids,
#which is not useful here

from cadquery import Shape,ShapeType

class TestSolid(Shape):
    def __init__(self,solid_id):
        Shape.__init__(self,solid_id,ShapeType.SOLID)
        self.s = None


def test_create():
    sl = ShapeLog()
    testid = "testID"
    THESOLID = TestSolid(testid)
    sl.log_shape_action(testid,ReferenceType.OPERATION,ActionType.CREATED, THESOLID )
    
    print sl.created_by_id(testid)
    assert sl.created_by_id(testid) == [ THESOLID ]
    assert sl.all() == [ THESOLID ]
    assert sl.all_solids() == [ THESOLID]
