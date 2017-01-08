"""
   Operation Results.
   
   Each operation produces a result, which details the changes that were
   made. 
   
   The structure is needed to support the createdBy, modifiedBy, and createdFrom
   selectors, which select geometry based on which operation created them
   or modified them ( a new CQ 2.0 feature)
   
   See backend_base for a list of the Operations that a backend is expected to provide
   
"""
from cadquery import ShapeLog

class BaseOperation(object):
    def __init__(self,id):
        self.id = id
        self.shape_log = ShapeLog()
        self.success = False
        self.result_message = None
        
    def set_result(self,success,message="OK"):
        self.success = success
        self.result_message = message
        
    def perform(self):
        r.set_result(False,"Not Implemented. Please subclass this. typically, this means create some geometry, add to shape_history, and set result")


        

    