"""
	Plate with a hole example,
	Using only CQ operations.
	
	One feature of CQ 2.0 operations is that they can be 
	used directly.
	
	When you are using the direct api, selectors are used like
	filters, and you are not using operation ids because you have
	programmatic access to the operation object itself.
	
	
"""
from cadquery import RectangleWire_Operation

#make a rectangle
rectangle = RectangleWire_Operation('rect1')
rectangle.set_mincorner(Vector(0,0,0))
rectangle.set_maxcorner(Vector(10,10,0))
rectangle.perform() 
created_wires = rectangle.created_shapes() # a list of CreatedShape objects

#make a face from the rectangle
face_from_wire = FaceFromWires_Operation('face')
face_from_wire.set_wires(created_wires)
face_from_wire.perform()
created_faces = face_from_wire.created_shapes()

#extrude the face to create a solid
#note how at this level you have direct control of the
#operation, such as whether it is a blind extrude or some other end condition
prism = Extrude_Operation('base-extrude')
prism.set_faces(created_faces)
prism.set_direction(Vector(0,0,1))
prism.set_blind_distance(0.5)
prism.perform()
created_solids = prism.created_shapes()

#make a cylinder 
cylinder = Cylinder_Operation('hole')
cylinder.set_radius(0.2)
cylinder.set_ends(Vector(5,5,0),Vector(5,5,1))
cylinder.perform()
created_holes = cylinder.created_shapes()

#cut the hole
cut = Cut_Operation('drill-hole')
cut.set_base_solids(created_solids)
cut.set_solids_to_cut(created_holes)

cut.perform() 

#select only faces that were created during the cut. This will be the cylindrical face of
# the hole only.
face_selector = TypeSelector(ShapeType.FACE)
hole_face = face_selector.filter(cut.created_shapes())










