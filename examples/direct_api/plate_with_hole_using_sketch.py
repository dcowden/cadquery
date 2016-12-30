"""
	Plate with a hole example,
	This example uses single extrude, and a sketch to make life simpler to create wires, but
	then we use the operations directly afterwards
	
	
"""
from cadquery import RectangleWire_Operation

#make a sketch
sketch = Sketch('base',Planes.XY)

sketch.rect('rect1',(0,0),(10,10)
sketch.circle('circle1'(5,5),0.2)
sketch.solve() # generates wires and faces and all that stuff

sketch_faces = sketch.solved_faces()

#extrude the face to create a solid
#note how at this level you have direct control of the
#operation, such as whether it is a blind extrude or some other end condition
prism = Extrude_Operation('base-extrude')
prism.set_faces(sketch_faces)
prism.set_direction(Vector(0,0,1))
prism.set_blind_distance(0.5)
op3_result = prism.perform()
created_solids = op3_result.created_shapes()

#select only faces that were created during the cut. This will be the cylindrical face of
# the hole only.
face_selector = TypeSelector(ShapeType.FACE)
hole_face = face_selector.filter(cut_result.created_shapes())










