from cadquery import Vector,Sphere_Operation


def test_simple_sphere():
    v = Vector(1.0,1.0,1.0)
    myid = "testsphere1"
    so = Sphere_Operation(myid,center=v, radius=2.0)
    so.perform()
    assert so.success

    generated = so.shape_log.created_by_id(myid)

    assert len(generated) == 1
    mysphere = generated[0]
    #assert mysphere.volume() > 0
