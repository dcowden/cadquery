# -*- coding: utf-8 -*-
"""
Base Context classes.
These classes provide the modelling framework itself

"""

# a modelling context. 
class Context(object):

    def __init__(self):
        
       self.operations = [] #operations, in the order they were executed
       self.shapes =[] # a list of top-level shapes that are defined
       self.sketches={} #key=sketchId, value=sketch object
       self.shapeHistory = ShapeHistory()
       

# tracks shapes and which ones were created by/updated by what operation

class ShapeHistory(object):
    def __init(self):
        
        self.operation_results = {} #key=operationId, results=shapelist

    def add_operation(self,operationResult):
        
        self.results.append(operationResult)
        
        #also here we need to update every operation result,
        #using the hashcode to update other isntances of the same
        #object in the history
        
    
# a collection of 2-d geometry that will be used to create 3D features
class Sketch(object):
    
    def __init__(self,sketch_id, plane):
        
        self.sketch_id = sketch_id
        self.plane = plane
        self.wires = []


    def add_wire(self,wire):
        self.wires.append(wire)
    

    def get_wires(self):
        raise NotImplementedError("Should return wires sorted from outer to inner")

