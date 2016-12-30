# -*- coding: utf-8 -*-
"""
Base Context classes.
These classes provide the modelling framework itself

    Context: tracks all of the activities in a single workspace.
    ShapeHistory: tracks history of the workspace, to enable queries based on how objects
       were created. 
    Sketch: an abstraction that makes it easier to create 3D geometry in a 2D plane

"""
from cadquery import ShapeType


# a modelling context. 
class Context(object):

    def __init__(self):
        self.shapes =[] # a list of top-level shapes that are defined
        self.sketches={} #key=sketchId, value=sketch object
        self.shape_history = ShapeHistory()
        self.id_generator= IdGenerator()
        
    def generate_id(self):
        return self.id_generator.generate_id()


class IdGenerator(object):
    def __init__(self):
        self.counter = 0
        
    def generate_id(self):
        self.counter += 1
        return self.counter

class ShapeHistory(object):
    """
        Stores a history of shapes and what happened to them:
        
        (a) which ones were created, modified, or deleted?
        (b) if available, what ID were they created or modified from? 
            -- note: sometimes the created from ID might be a shape, but sometimes
               it could be a sketchID or operation ID. thats why they are ids
               
        This object needs to support a query-like interface
        
        It is worth noting that a single shape may have more than one reference entry.
        For example, a face may have been modified from a previous face, and also created by a given operation id
    """
    def __init__(self):
        self.shapes = {} # shape id, shape
        self.refs = [] #we may need to tune this in the future for performance, but this meets the need for now
        
    def add_shape_reference(self,reference_type,action_type,shape):
        self.refs.append( ReferenceEntry(id,reference_type,action_type,shape))

    def merge_history(self, another_history):
        # merges another history into this one
        for ref in another_history.refs:
            self.refs.append( ref)

    def query(self, action_type=None, for_id=None, reference_type=None, shape_type=None):
        query_results = []
        for r in self.refs:
            matches = True
            if action_type is not None and r.action_type != action_type :
                matches = False
            if reference_type is not None and r.reference_type != reference_type :
                matches = False
            if for_id is not None and r.id != for_id :
                matches = False
            if shape_class is not None and r.shape.shape_type != shape_type :
                matches = False             
            if matches:
                query_results.append(r)
                
        return query_results
    
    def all_shapes(self):
        s = set()
        for r in self.refs:
            s.add(r.shape)
        return s
    
    def created_faces(self):
        return self.query(action_type=ActionType.CREATED,shape_type=ShapeType.FACE)
        
    def created_shapes(self):   
        return self.query(action_type=ActionType.CREATED)
        
    def modified_shapes(self):
        return self.query(action_type=ActionType.MODIFIED)
        
    def deleted_shapes(self):
        return self.query(action_type=ActionType.DELETED)
        
    def created_by_id(self,id):
        return self.query(action_type=ActionType.CREATED,for_id=id)
        
    def modified_by_id(self):
        return self.query(action_type=ActionType.MODIFIED,for_id=id)
        
class ReferenceEntry(object):
    def __init__(self,id,reference_type,action_type,shape):
        self.id = id
        self.reference_type = reference_type
        self.action_type = action_type
        self.shape = shape
    
class ActionType(object):
    CREATED="CREATED"
    MODIFIED="MODIFIED"
    DELETED="DELETED"
    
class ReferenceType(object):
    SKETCH="SKETCH"
    OPERATION="OPERATION"
    SHAPE="SHAPE"



    