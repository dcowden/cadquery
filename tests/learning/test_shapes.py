import pytest

import OCC
from OCC.BRepPrimAPI import *
from OCC.gp import *
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse,BRepAlgoAPI_Cut
from OCC.Display.SimpleGui import *

from OCC.TopoDS import topods, TopoDS_Edge, TopoDS_Compound
from OCC.TopExp import TopExp_Explorer
from OCC.TopAbs import TopAbs_EDGE, TopAbs_FACE,TopAbs_SOLID
from OCC.TopTools import TopTools_ListOfShape,TopTools_ListIteratorOfListOfShape
from OCC.BRep import BRep_Tool_Surface
from OCC.Geom import Geom_Plane, Geom_CylindricalSurface, Handle_Geom_Plane, Handle_Geom_Surface

SEED=757575757


def face_is_plane(face):
    """
    Returns True if the TopoDS_Shape is a plane, False otherwise
    """
    hs = BRep_Tool_Surface(face)
    downcast_result = Handle_Geom_Plane.DownCast(hs)
    # The handle is null if downcast failed or is not possible, that is to say the face is not a plane
    if downcast_result.IsNull():
        return False
    else:
        return True


def getFaces(shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    faces = []
    while explorer.More():
        f = topods.Face(explorer.Current())
        faces.append(f)
        explorer.Next()  
    return faces

def getEdges(shape):
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    edges = []
    while explorer.More():
        e = topods.Edge(explorer.Current())
        edges.append(e)
        explorer.Next()  
    return edges
    
def getSolids(shape):
    explorer = TopExp_Explorer(shape, TopAbs_SOLID)
    solids = []
    while explorer.More():
        f = topods.Solid(explorer.Current())
        print f.HashCode(SEED),f
        solids.append(f)
        explorer.Next()  
    return solids

def occListToList(occList):
    r = []
    i = TopTools_ListIteratorOfListOfShape(occList)
    while i.More():
        r.append(i.Value())
        i.Next()
    return r
    
def printShape(shape):
    st = shape.ShapeType()
    
    if st == 4:
        print "Face: %s " % ( shape.HashCode(SEED))
    elif st == 6:
        print "Edge: %s " % ( shape.HashCode(SEED))
    elif st == 2:
        print "Solid: %s" % ( shape.HashCode(SEED))
    else:
        print "Unkown Type(%d): %s" % (st, shape.HashCode(SEED))
    

def printShapeList(shapeList):
    for s in shapeList:
        printShape(s)
        
@pytest.mark.skip(reason="Only if yoyu want to see some OCC details")
def test_occ_shapes():
    ax1 = gp_Ax2(gp_Pnt(0,0,0), gp_DZ() )
    c1 = BRepPrimAPI_MakeCylinder(ax1, 20, 20 )
    #print "Cylinder:",c1.Shape().HashCode(SEED),c1.Shape().ShapeType()
    printShape(c1.Shape() )
    print "Faces of cylinder1:" 
    f1 = getFaces(c1.Shape())
    e1 = getEdges(c1.Shape())
    printShapeList(f1)
    print "Edges of cylinder1:"
    printShapeList(e1)
    
    ax2 = gp_Ax2(gp_Pnt(0,0,0), gp_DZ() )
    c2 = BRepPrimAPI_MakeCylinder(ax2,5,5 )
    printShape(c2.Shape())
    print "Faces of cylinder2:" 
    f2 = getFaces(c2.Shape())
    e2 = getEdges(c2.Shape())
    printShapeList(f2)
    print "Edges of cylinder2:"
    printShapeList(e2)
    
    
    c3 = BRepAlgoAPI_Cut(c1.Shape(), c2.Shape() )
    printShape(c3.Shape())
    print "Faces of cylinder3:" 
    f3 = getFaces(c3.Shape())
    e3 = getEdges(c3.Shape())
    printShapeList(f3)
    print "Edges of cylinder3:"
    printShapeList(e3)
    
    
    print "Modified By Results:"
    
    print "Modified from c1", printShapeList( occListToList(c3.Modified(c1.Shape())))
    print "Modified from c2", printShapeList( occListToList(c3.Modified(c2.Shape())))
    for f in f1:
        print "Modified from ",printShape(f),printShapeList(occListToList(c3.Modified(f)))
    for f in f2:
        print "Modified from ",printShape(f),printShapeList(occListToList(c3.Modified(f)))
    for e in e1:
        print "Modified from ",printShape(e),printShapeList(occListToList(c3.Modified(e)))
    for e in e2:
        print "Modified from ",printShape(e),printShapeList(occListToList(c3.Modified(e)))
    
        
    #print c3.HasDeleted(), c3.HasGenerated(), c3.HasModified()
    #ol = occListToList(c3.Modified(f1[2]))
    #print "Face ",ol[0].HashCode(SEED),"is modified version of face",f1[2].HashCode(SEED) 
    
    #f3 = getFaces(c3.Shape())
    #solids= getSolids(c3.Shape() )
    #for s in solids:
    #    print s.HashCode(SEED)
        
    #print "Faces of Resulting Body"
    #print "hashcode,shapetype,modified,orientation,convex,isplane"
    #for f in f3:
    #    print f.HashCode(SEED),f.ShapeType(),f.Modified(),f.Orientation(),f.Convex(),face_is_plane(f)
