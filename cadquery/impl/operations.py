from cadquery import BaseOperation


from cadquery import ShapeLog,ActionType,ReferenceType,Solid
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.gp import gp_Pnt
import traceback

#Primitive Operations
class Sphere_Operation(BaseOperation):
    
    def __init__(self, id,center=None,radius=None):
        BaseOperation.__init__(self,id)
        #TODO: add angles and angle options  as well.
        self.center = center
        self.radius = radius

    def perform(self):

        try:
            #perform the operation
            vec = self.center.v
            center_pt = gp_Pnt(vec.X(), vec.Y(), vec.Z())       
            op = BRepPrimAPI_MakeSphere(center_pt,self.radius)
            op.Build()
            result_shape = op.Shape()
            created_sphere = Solid( result_shape)

            #register the result in shape log
            #in this case its pretty easy, we just generated  sphere
            self.shape_log.log_shape_action(self.id,ReferenceType.SHAPE, ActionType.CREATED, created_sphere)
            self.success = True
            self.result_message="OK"
        except Exception as ex:
            traceback.print_exc()
            self.success = False
            self.result_message = ex.message


class Cone_Operation(BaseOperation):pass
class Wedge_Operation(BaseOperation):pass
class Box_Operation(BaseOperation):pass
class Torus_Operation(BaseOperation):pass
class Cylinder_Operation(BaseOperation):pass

#Solid Operations
class Extrude_Operation(BaseOperation): pass
class Revolve_Operation(BaseOperation): pass
class Sweep_Operation(BaseOperation): pass
class Loft_Operation(BaseOperation): pass
class Draft_Operation(BaseOperation): pass
class Union_Operation(BaseOperation): pass
class Intersect_Operation(BaseOperation): pass
class Cut_Operation(BaseOperation): pass
class Chamfer_Operation(BaseOperation): pass
class SplitOperation(BaseOperation):pass
class Fillet_Operation(BaseOperation): pass
class Clean_Operation(BaseOperation): pass
class Hole_Operation(BaseOperation): pass
class Cbore_Operation(BaseOperation): pass
class Countersink_Operation(BaseOperation): pass

#Transformations
class Rotate_Operation(BaseOperation): pass
class Translate_Operation(BaseOperation): pass
class Tranform_Operation(BaseOperation):pass

#Face Operations
class FaceCut_Operation(BaseOperation):pass
class FaceIntersect_Operation(BaseOperation):pass
class FaceFromPlane_Operation(BaseOperation):pass
class FuseFace_Operation(BaseOperation):pass
class RuledSurface_Operation(BaseOperation):pass
class FaceFromWires_Operation(BaseOperation):pass

#Edge Operations
class CircleEdge_Operation(BaseOperation): pass
class SplineEdge_Operation(BaseOperation): pass
class Edge_Operation(BaseOperation): pass
class PolyLineEdge_Operation(BaseOperation):pass
class ThreePointArc_Edge_Operation(BaseOperation):pass
class CenterPointArc_Edge_Operation(BaseOperation):pass

#Wire Operations
class CircleWire_Operation(BaseOperation): pass
class RegularPolygonWire_Operation(BaseOperation):pass
class Helix_Operation(BaseOperation):pass
class CombineWires_Operation(BaseOperation):pass
class CombineEdges_Operation(BaseOperation):pass
class RectangleWire_Operation(BaseOperation):pass

#Shell Operations
class ShellFromFaces_Operation(BaseOperation): pass
class ShellSolid_Operation(BaseOperation): pass

#Projection Operations
class ProjectOntoPlane_Operation(BaseOperation): pass

#Other Stuff
class Combine_Operation(BaseOperation): pass
