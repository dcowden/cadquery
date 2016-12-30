from cadquery import Vector,Direction


def test_DX():
    assert Direction.X == Vector(1.0,0,0)