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
        #in process sketches, key=sketchId, value=sketch object
        #sketches do not generate shapes in the context until they are solved
        self.sketches={} #
        
        #stores the history of all shapes and operations, so that we can support queries
        self.shape_log = ShapeLog()
        
        #all of the operations that happened
        self.operations = []
        
        #auto-generate ids when needed
        self.id_generator= IdGenerator()


class IdGenerator(object):
    """
        Returns ids like 'extrude1' or 'line2'. 
        Each prefix gets its own counter series
    """
    def __init__(self):
        self.counters = {}
        
    def generate_id(self,prefix=""):
        c = self.counters.setdefault(prefix,0) + 1
        self.counters[prefix] = c
        return "%s%d" % ( prefix, c )

class ShapeLog(object):
    """
        Stores a history of shapes and what happened to them.
        Also provides a current list of the active shapes. 
        IE, shapes that have been created but not deleted
        
        Its kind of like a git repository for shapes.
        
        (a) which ones were created, modified, or deleted?
        (b) if available, what ID were they created or modified from? 
            -- note: sometimes the created from ID might be a shape, but sometimes
               it could be a sketchID or operation ID. thats why they are ids
        (c) what shapes are currenly active in the context
               
        This object needs to support a query-like interface
        
        It is worth noting that a single shape may have more than one reference entry.
        For example, a face may have been modified from a previous face, and also created by a given operation id
    """
    def __init__(self):
        self.shapes = {} # shape id, shape
        
        #we may need to tune this in the future for performance, but this meets the need for now
        self.actions = [] 
        
    def log_shape_action(self,ref_id,reference_type,action_type,shape):
        self.actions.append( ReferenceEntry(ref_id,reference_type,action_type,shape))

    def merge_log(self, another_log):
        # merges another log into this one
        for ref in another_log.actions:
            log_shape_action(ref)

    def query(self, action_type=None, for_id=None, reference_type=None, shape_type=None):
        """
            Query for objects by how they were created, what object they were created from, what type,
            etc.
            
            All queries imply the condition 'objects that are still alive'.  Objects that have been removed
            will never be returned, though the operations that created them may remain to allow other queries
            to return results.
            
            Example:
                 
                We create a Plate using operation 'plate1', and then a cylinder, using 'cylinder-1'
                and we subtract the cylinder from the plate in operation 'subtract1'
                
                Here are some queries and what they return in this case:
                
                all solids: the plate with the hole in it
                all faces: the faces of the plate with the hole in it
                faces created by 'subtract1' will be the cylindrical face in the hole of the plate
                faces modified by 'subtract1' will be the top and bottom faces of the plate (since they were modified during the cut)
                
        """
        query_results = {}
        for r in self.actions:
            matches = True
            if action_type is not None and r.action_type != action_type :
                matches = False
            if reference_type is not None and r.reference_type != reference_type :
                matches = False
            if for_id is not None and r.ref_id != for_id :
                matches = False
            if shape_type is not None and r.shape.shape_type != shape_type :
                matches = False             
            if matches:
                query_results[r.shape.sid] = r.shape
                
        return query_results.values()
    
    def all(self):
        return self.query()
        
    def all_solids(self):
        return self.query(shape_type=ShapeType.SOLID)
        
    def all_faces(self):
        return self.query(shape_type=ShapeType.FACE)
        
    def created_by_id(self,created_by_id):
        return self.query(action_type=ActionType.CREATED,for_id=created_by_id)
        
    def modified_by_id(self,modified_by_id):
        return self.query(action_type=ActionType.MODIFIED,for_id=modified_by_id)
        
class ReferenceEntry(object):
    def __init__(self,refid,reference_type,action_type,shape):
        self.ref_id = refid
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



    