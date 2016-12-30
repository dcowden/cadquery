"""
     a collection of 2-d geometry that will be used to create 3D features
     sketch methods use x,y tuples because
     all operations are in 2-d space of the sketch plane ( unless otherwise stated )

     TODO: key design note:
       we need to be able to run selectors on objects in the sketch before the sketch
       is completed, for example if we want to project an entity onto the sketch and
       after that select those to get their coordinates

     sketch entities are used because in the future they
     will be part of the 2d sketch solver.
     in the meantime, they are converted directly to geometry

     for that reason, they are part of the implementation now. IE, that's why
     when we sketch we'll use sketch entities, rather than directly creating Vectors, Wires, and so on.
     
     Until we have a solver, we'll simply support only syntax where a direct conversion can be made

"""
from cadquery import ShapeLog

def validate_is_tuple_2d(value,allowNone=False):
    if allowNone and value is None:
        return
    if value.__class__ is not tuple or len(value) != 2:
        raise ValueError("Expected 2-tuple, received %s" % value)

class Sketch(object):
    """
        From Workplane in CQ 1.X
        
        A 2-d modelling context with a given coordinate system
        The sketch object supports CQ 2.0 notions of constraint-based sketching,
        But does NOT include the fluent api features like moveTo and lineTo, which
        are still located in Workplane.
        
    """
    def __init__(self,sketch_id, plane):
        
        self.sketch_id = sketch_id
        self.plane = plane
        self.sketch_entities = {} # id, entity object
        self.shape_log = ShapeLog()
        
    def add_entity(self, sketch_entity):
        self.entities[sketch_entity.id] = sketch_entity
    
    def add_constraint(self, sketch_constraint):
        raise NotImplementedError("Constraints not supported yet")
        
    def rect(self,id,min_corner_tuple, max_corner_tuple,forConstruction=False):
        pass
    
    def line(self,id,from_tuple,to_tuple,forConstruction=False):
        """
          supports Workplane.line, Workplane.vline, Workplane.hline, Workplane.lineTo, Workplane.vLineTo, Workplane.hLineTo
        """
        pass

    def spline(self,id,listOfXYTuple,forConstruction=False):
        pass
        
    def mirrorX(self):
        pass
    
    def mirrorY(self):
        pass
        
    def circle(self,id,center_tuple,radius,forConstruction=False):
        pass
        
    def project(self,id,shape):
        pass
        #attempt to project a shape onto this sketch
   
    def rarray(self, xSpacing, ySpacing, xCount, yCount, center=True):
        # create rectangular array of points
        # originally: Workplane.rarray
        """
        if xSpacing < 1 or ySpacing < 1 or xCount < 1 or yCount < 1:
            raise ValueError("Spacing and count must be > 0 ")

        lpoints = []  # coordinates relative to bottom left point
        for x in range(xCount):
            for y in range(yCount):
                lpoints.append((xSpacing * x, ySpacing * y))

        #shift points down and left relative to origin if requested
        if center:
            xc = xSpacing*(xCount-1) * 0.5
            yc = ySpacing*(yCount-1) * 0.5
            cpoints = []
            for p in lpoints:
                cpoints.append((p[0] - xc, p[1] - yc))
            lpoints = list(cpoints)

        return self.pushPoints(lpoints)
        """
    
    def transform(self, angle_tuple, offset_tuple):
        # rotate and/or offset this sketch coordinate system around the normal vector
        # was originally: Workplane.transformed
        pass
        
    def solved_faces(self):
        #only available after the sketch is solved. Maybe there's a better way to do this?
        return self.shape_log.created_faces()
        
    def solve(self):
        SketchSolver.solve(self)

class SketchEntity(object):
    def __init__(self,id,construction=False):
        #used later in the fluent api to list constraints
        self.id = id
        self.construction = construction

class SketchPoint(SketchEntity):
    def __init__(self,id,construction=False,location=None):
        SketchEntity.__init__(self)
        validate_is_tuple_2d(location,allowNone=False)
        self.location=location
    
class SketchLine(SketchEntity):
    def __init__(self,id,construction=False,from_location=None, to_location=None):
        SketchEntity.__init__(self)
        
        validate_is_tuple_2d(from_location,allowNone=False)
        validate_is_tuple_2d(to_location,allowNone=False)
        self.from_location=from_location
        self.to_location = to_location

class SketchCircle(SketchEntity):
    def __init__(self,id,construction=False,center=None, radius=None):
        SketchEntity.__init__(self)
        validate_is_tuple_2d(center,allowNone=False)
        self.center=center
        self.radius = float(radius)
        
    
class SketchCenterpointArc(SketchEntity):
    pass

class SketchThreePointArc(SketchEntity):
    def __init__(self,id,construction=False,first_point=None, middle_point=None,last_point=None):
        SketchEntity.__init__(self)
        validate_is_tuple_2d(first_point,allowNone=False)
        validate_is_tuple_2d(middle_point,allowNone=False)
        validate_is_tuple_2d(last_point,allowNone=False)
        self.first_point=first_point
        self.middle_point=middle_point
        self.last_point=last_point
    
class SketchSpline(SketchEntity):
    def __init__(self,id,construction=False):
        raise NotImplementedError("Spline not implemented yet")

class SketchConstraint(object):
    def __init__(self,id):
        self.id = id
        raise NotImplementedError("Constraints are not implemented yet")
        
class EqualConstraint(SketchConstraint):
    pass
    
class ParallelConstraint(SketchConstraint):
    pass
    
class PerpendicularConstraint(SketchConstraint):
    pass

class DistanceConstraint(SketchConstraint):
    pass

class AngleConstraint(SketchConstraint):
    pass

class LengthConstraint(SketchConstraint):
    pass

class SymmetricConstraint(SketchConstraint):
    pass

class ConcentricConstraint(SketchConstraint):
    pass



class SketchSolver(object):
    """
        Solves a sketch, and produces a set of wires and/or edges.
        Until we have a real solver, we'll simply require fixed- location 
        geometry only rather than supporting constraints.
        But the system will work the same anyway
        
        When a sketch is solved, it produces a set of wires and edges,
        which can then be added to the modelling context
        
        Each sketch entity has an id, so that it is possible to relate which
        sketch entities created which wires and edges and faces
        
    """
    def solve(self, sketch):
        #solve the sketch. 
        #1. convert sketch entities to wires, edges, and faces
        #2. add the created items to the shape history for the sketch
        
        #for now, we simply require that all things are fully qualified, so that we can 
        #trivially solve the sketch
        pass


