"""
    Backend must implement all of the operations.
    The implemented name must be the same as the 
    base one, but without the 'Base' prefix.
    
    If a backend does not support an operation, it should
    still provide an implementation, but raise an error
    in the perform method.
    
    TODO: there might be a better way to do this.
    Sometimes, backends may not be ab

    To implement this, you'll probably need these two references:

    https://www.opencascade.com/doc/occt-7.1.0/refman/html/index.html

    http://api.pythonocc.org/index.html

"""
from cadquery.impl_base.operations import *
from cadquery import ShapeLog,ActionType,ReferenceType,Solid
from OCC.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.gp import gp_Pnt
import traceback

class Sphere_Operation(BaseSphere_Operation):
    
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


