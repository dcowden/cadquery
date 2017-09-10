Direct API
==============

Thoughts on the direct api.  The new direct api of CQ 2.0 is designed to be easy to use, and more direct than the fluent api.  Most likely, the fluent api will be implemented in terms of the direct api.


Inspirations
================
This way of working incorporates ideas from several other systems:
  * CQ 1.x (obviously)
  * django ORM, which has the concept of queries ( thanks @fragmuffin)
  * OpenCascade, which itself heavily relies upon Operations to do work
  * https://github.com/dcowden/cadquery/issues/167 ( thanks to all who contributed)
  
Sample Parts
===============
Here are a couple of use cases that make discussion easier

**Chamfer-hole**
  1. Start with a box
  2. Draw a circle on the top face, and extrude it to make a cylindrical cut
  3. chamfer the edge on the top face that was created by the cut operation

  ![](https://github.com/dcowden/cadquery/raw/2_0_occ/examples/direct_api/chamfer-cut.png)

**Layer Cake**
  1. extrude a circle
  2. extrude another circle starting from the top face of the previous one
  ![](https://github.com/dcowden/cadquery/raw/2_0_occ/examples/direct_api/layercake.png)

Key Objects and Concepts
==========================
There are a number of objects/concepts relevant regardless of the api used:

 *Context* The modelling context contains all of the objects in a modelling space. A context tracks all of the shapes created within it. Creating a new context essentially starts with a clean slate. It is possible to swtich between apis by sharing the same context, which allows different api versions ( including older versions of the context) to interoperate

 *Shape* A concrete topological object, such as a solid, face, edge, compound, or plane. A shape is immutable-- any changes are always represented as a newly created shape.

 *Selector* Selects one or more shapes within a context. A selector has methods to filter objects by their type, generating operation, position, or other characteristics, and to eventually provide access to the underlying Shapes. Selectors are always connected to a single context. A selector may expose its own fluent or direct api

 *Geometry* A construct that underlies a shape, such as a plane, arc, axis, vector line, spline, or surface

 *Operation* Creates, modifies, or deletes Shapes within a context.  Operations are low-level constructs that accept shapes and geometry, and manipulate/produce more geometry and shapes. This makes them easy to code and test in terms of the underlying provider ( pythonOCC/FreeCAD). Operations are also responsible for tabulating which shape topology changed during the operation, to support selectors based on this information.  Some providers, like FreeCAD, do not expose the information needed to track which shape topology changed as a result of an operation, but others (pythonOCC) do.

 *Sketch* A set of geometry on a 2-d plane that can be transformed by extrusion or sweeping into 3-d shapes.  Ideally, we will support a 2-d solver to make sketching easier. Sketch methods generally create sketch entities and return the corresponding sketch entitiy

 *API* Accepts a context and facilitates executing operations and running queries within a context.  At least two apis will be supported-- a fluent api and a direct api. Methods in the api typically perform one operation, but this is not always the case. Api methods generally return selectors and fluent api objects, rather than directly returning shapes.
 

The overall relationships of the key objects
=============================================

The basic way of working is as follows:

  * All work starts with creation of a context.
  * After creating a context, the next step is to create an api, which allows using a context. An api can be created in one step using a new context if desired.
  * the user may extend the api by adding operations from either local code, or by importing web modules
  * the user calls methods in the api. 
     * methods in the fluent api will return a reference to the fluent object, as in CQ 1.x
     * methods in the direct api will generally return a selector for the reults of the operation performed



Direct API Example
==================

    import cq
    from cq import Point,Axis

    # create a context and then an api ( in this case the direct api)    
    # cq.direct_api() is a shortcut for cq.direct_api(cq.new_context())    
    ctx = cq.direct_api()
    
    # we could create a fluent api and access the same objects available also...
    fluent_context = cq.fluent_api(ctx.context)
    
    
    # import other operations and add them to the direct api
    ctx.import_operation('https://some/other/module.py')
    
    # import and register a locally defined operation
    # operations return boolean for success/failure, and 
    # record
    class Intersect_Operation(BaseOperation):
        def evaluate(self,shape1, shape2 ):
            shape3 = shape1 intersect shape2
            self.log.created(shape3)
            self.log.modified(..some faces of shape3.. )
            return true
            
    ctx.register_operation(Custom_Operation, 'my_operation')

    # creating the chamfer-hole example. 
    # box is a selector that contains the resulting solid, and provides methods like faces() to select and traverse its topology
    box = ctx.box(1,2,0.5)
    
    # make a sketch on the top of the box,
    # centered on the midpoint of the rightmost edge
    # note that the selector methods themselves are a fluent api
    sketch_plane=box.faces('>Z')
    sketch_midpoint=box.faces('>Z').edges('>X').midpoint()
    
    # upon exiting the with block constraints are solved
    with cq.Sketch(sketch_plane, sketch_midpoint) as sketch:  
         c1 = sketch.circle(0.5)
         sketch.add_coincident(c1.center, sketch.origin)

    # cut a hole using the sketch    
    box_with_hole = ctx.cut_thru_all(sketch)
    
    # at this point, the old solid is still in the tree, referended by box
    # the new solid has 8 faces, one of which is cylindrical
    
    assert len(box.faces()) == 6
    assert len(box_with_hole.faces()) == 8
    
    # in the new solid, 1 face was created, 2 were modified, the others are the same as they were
    assert len(box_with_hole.faces("created")) == 1
    assert len(box_with_hole.faces("modified")) == 2
    
    # last step-- chamfer the edge top edge. 
    # make use of the selector api to select the upper edge of the cylindrical face
    chamfered_hole = ctx.chamfer(box_with_hole.faces("created").edges(">Z"))

    #some assertions
    assert len(chamfered_hole.solids()) == 1
    assert chamfered_hole != box_with_hole
    assert chamfered_hole.solids().first() != box_with_hole.solids().first()
    assert len(chamfered_hole.faces() == 9
    
More about What the Direct API is doing
=========================================

Consider a cut operation, which accepts two Solids:

    cut = Cut_Operation(solid1=some_solid, solid2=another_solid)
    cut.perform()
    shape_log = cut.shape_log

The shape_log gives a list of all of the topology items that were created, modifed, or destroyed in the operation.

The direct api exposes this operation by providing a method which expects queries, and returns a query, for example

    def cut( source_query, tools_query):

        shape_log = self.context.shape_log

        operation_id = self.id_generator.newId()

        #get a single source solid to subtract from
        source_solid = source_query.solids().first().evaluate()

        #get a list of tool solids
        tool_solids = source_query.solids().evaluate()

        for tool in tool_solids:
            cut = Cut_Operation(solid1=source_solid, solid2=tool)
            cut.perform()

            #merge information about what objects were modified into the tree.
            #this is how we track the magic of what objects became what.            
            shape_log.merge(cut.shape_log)    
        
        #return a query that can be used to select any shapes created, modified, or deleted by this operation
        return Query(self.ctx).filter(operationId=operation_id)
