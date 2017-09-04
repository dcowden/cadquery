Direct API
==============

Thoughts on the direct api.  The new direct api of CQ 2.0 is designed to be easy to use, and more direct than the fluent api.  Most likely, the fluent api will be implemented in terms of the direct api.

Key Objects and Concepts
==========================
There are a number of objects/concepts relevant regardless of the api used:

 *Context* The modelling context contains all of the objects in a modelling space. A context tracks all of the shapes created within it. Creating a new context essentially starts with a clean slate.

 *Shape* A concrete topological object, such as a solid, face, edge, compound, or plane.

 *Query* Can select one or more shapes from within a context. A query will always select one or more shapes. Queries have a number of filters used to select shapes, including the shape type, the operation id, whether the shape was created, modified, or deleted, shape position, orientation, location, etc.

 *Geometry* A construct that underlies a shape, such as a plane, arc, axis, vector line, spline, or surface

 *Operation* Creates, modifies, or deletes Shapes within a context.  Operations are low-level constructs that accept shapes and geometry, and manipulate/produce more geometry and shapes. This makes them easy to code and test in terms of the underlying provider ( OCC). Operations will generally not involve the context or queries. Operations manipulate one or more objects, and provide information on what shapes have been created, deleted, or modified.

 *Sketch* A set of geometry on a 2-d plane that can be transformed by extrusion or sweeping into 3-d shapes.  Ideally, we will support a 2-d solver to make sketching easier

 *API* Accepts a context and facilitates executing operations and running queries within a context.  At least two apis will be supported-- a fluent api and a direct api. Methods in the direct api typicaly accept queries, and return queries that can be used to explore the resulting geometry

The overall relationships of the key objects
=============================================

The basic way of working is as follows:

  * All work starts with creation of a context. A context 
  * After creating a context, the next step is to create an api, which allows using a context
  * using an api, the user will execute operations.
  * The user will use the queries produced by the operations to build up a model

Inspirations
================
This way of working incorporates ideas from several other systems:
  * CQ 1.x (obviously)
  * django ORM, which has the concept of queries ( thanks @fragmuffin)
  * OpenCascade, which itself heavily relies upon Operations to do work

Direct API Example
===============

    import cq
    from cq import Point,Axis

    #creating a new context creates an empty workspace
    ctx = cq.new_context()

    #all direct api calls using this object now operate in this context
    dapi = cq.direct_api(ctx)

    #create a box with lower corner at origin, with dimensions, 10,10, and 1 unit
    #note that a workplane is not required in the direct api
    q_box = dapi.box( Point.Origin,10,10,10 )

    #select all solids created by the box operation, which in this case is just the box

    #when box is called, an Operation is created and executed
    #q_box is a query that can be used to select objects modified, created, or deleted by this operation

    #created_solids is still a query.
    created_solids = q_box.created().solids()
    created_faces = q_box.created().faces()

    #Evaluating queries returns the actual underlying shapes:
    list_of_solids = q_box.created().solids().evaluate()

    #create another box, which overlaps the prior one
    another_box = dapi.box(Vector(5,0,0), 20,20,20)

    #subtract the second from the first
    #the subtract operation accepts queries that must return solids.
    #all of the solids that match the second query are subtracted from all those that match
    #the first query. 
    half_box = dapi.subtract(q_box.solids(),another_box.solids())

    #now the need for queries starts to become clear.
    #the half-box is actually a modified version of the original box,
    #so they point to the same object
    assert half_box.modified().solids() == created_solids

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
