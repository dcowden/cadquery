"""
   Operation Results.
   
   Each operation produces a result, which details the changes that were
   made. 
   
   The structure is needed to support the createdBy, modifiedBy, and createdFrom
   selectors, which select geometry based on which operation created them
   or modified them ( a new CQ 2.0 feature)
   
   See backend_base for a list of the Operations that a backend is expected to provide
   
"""

class OperationResult(object):
    def __init__(self):
        self.created = []
        self.modified = []
        self.deleted = []
        self.success = False
        self.result_message = None
        
    def add_modified(self,modified_shape,original_shape=None):
        self.modified.append( ModifiedShape(modified_shape,original_shape))
        
    def add_created(self,created_shape, created_from_shape=None):
        self.created.append ( CreatedShape(created_shape,created_from_shape))
        
    def add_deleted(self,deleted_shape):
        self.deleted.append ( DeletedShape(deleted_shape))
        
    def set_result(self,success,message="OK"):
        self.success = success
        self.result_message = message

class ModifiedShape():
    def __init__(self,original_shape,modified_shape=None):
        self.original = original_shape
        self.modified = modified_shape
        
class CreatedShape():
    def __init__(self,created_shape,created_from_shape=None):
        self.created_from = created_from_shape
        self.created = created_shape

class DeletedShape():
    def __init__(self,deleted_shape):
        self.deleted = deleted_shape

class BaseOperation(object):
    def __init__(self,id):
        self.id = id

    def perform(self):
        r= OperationResult()
        r.set_result(False,"Not Implemented. Please subclass this and do some work")
        return r


