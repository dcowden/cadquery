# -*- coding: utf-8 -*-
"""
    Tools for Exporting and Importing
    We handle creating Three.js, AMF, and STL from a Mesh
"""

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

    
 

class ExportTypes:
    STL = "STL"
    STEP = "STEP"
    AMF = "AMF"
    SVG = "SVG"
    TJS = "TJS"
    BIN = "BINARY"

class UNITS:
    MM = "mm"
    IN = "in"

class Mesh(object):
    def __init__(self):

        self.vertices = [];
        self.faces = [];
        self.nVertices = 0;
        self.nFaces = 0;

    def add_vertex(self,x,y,z):
        self.nVertices += 1;
        self.vertices.extend([x,y,z]);

    #add triangle composed of the three provided vertex indices
    def add_triangle_Face(self, i,j,k):
        #first position means justa simple triangle
        self.nFaces += 1;
        self.faces.extend([0,int(i),int(j),int(k)]);

        
def exportShape(shape,exportType,fileLike,tolerance=0.1):
    """
        :param shape:  the shape to export. it can be a shape object, or a cadquery object. If a cadquery
        object, the first value is exported
        :param exportFormat: the exportFormat to use
        :param tolerance: the tolerance, in model units
        :param fileLike: a file like object to which the content will be written.
        The object should be already open and ready to write. The caller is responsible
        for closing the object
    """

    if exportType == ExportTypes.AMF:
        mesh = ExportMethods.export_mesh(shape)
        aw = AmfWriter(mesh,fileLike)
        aw.export_amf()
        
    elif exportType == ExportTypes.STEP:
        ExportMethods.export_step(shape,fileLike)
    
    elif exportType == ExportTypes.TJS:
        mesh = ExportMethods.export_mesh(shape)
        jw = JsonWriter(mesh,fileLike)
        jw.export_json()

    elif exportType == ExportTypes.SVG:
        ExportMethods.export_step(shape,fileLike)
        
    elif exportType == ExportTypes.BINARY:
        ExportMethods.export_Binary(shape,fileLike)

    elif exportType == ExportTypes.STL:
        mesh = ExportMethods.export_mesh(shape)
        aw = StlWriter(mesh,fileLike)
        aw.export_stl()
    else:
        raise NotImplementedError("Unknown Export Type")
        #binary output
        #all these types required writing to a file and then
        #re-reading. this is due to the fact that FreeCAD writes these
        (h, outFileName) = tempfile.mkstemp()
        #weird, but we need to close this file. the next step is going to write to
        #it from c code, so it needs to be closed.
        os.close(h)

        if exportType == ExportTypes.STEP:
            shape.exportStep(outFileName)
        elif exportType == ExportTypes.STL:
            shape.wrapped.exportStl(outFileName)
        else:
            raise ValueError("No idea how i got here")

        res = readAndDeleteFile(outFileName)
        fileLike.write(res)
    
    
def readAndDeleteFile(fileName):
    """
        read data from file provided, and delete it when done
        return the contents as a string
    """
    res = ""
    with open(fileName,'r') as f:
        res = f.read()

    os.remove(fileName)
    return res


def guessUnitOfMeasure(shape):
    """
        Guess the unit of measure of a shape.
    """
    bb = shape.BoundBox

    dimList = [ bb.XLength, bb.YLength,bb.ZLength ]
    #no real part would likely be bigger than 10 inches on any side
    if max(dimList) > 10:
        return UNITS.MM

    #no real part would likely be smaller than 0.1 mm on all dimensions
    if min(dimList) < 0.1:
        return UNITS.IN

    #no real part would have the sum of its dimensions less than about 5mm
    if sum(dimList) < 10:
        return UNITS.IN

    return UNITS.MM    
    
class JsonWriter(object):
    def __init__(self,mesh):
        self.mesh= mesh
        
    def export_json(self,out_file):
        return JSON_TEMPLATE % {
            'vertices' : str(self.mesh.vertices),
            'faces' : str(self.mesh.faces),
            'nVertices': self.nVertices,
            'nFaces' : self.nFaces
        };

"""
    We control this because some backends produce bad STL
"""
class StlWriter(object):
    def __init__(self,mesh):
        self.mesh= mesh
        
    def export_stl(self,out_file):
        raise NotImplementedError("Please implement this core cq function")
        
class AmfWriter(object):
    def __init__(self,mesh):

        self.units = "mm"
        self.tessellation = mesh

    def export_amf(self,outFile):
        amf = ET.Element('amf',units=self.units)
        #TODO: if result is a compound, we need to loop through them
        object = ET.SubElement(amf,'object',id="0")
        mesh = ET.SubElement(object,'mesh')
        vertices = ET.SubElement(mesh,'vertices')
        volume = ET.SubElement(mesh,'volume')

        #add vertices
        for v in self.mesh.vertices:
            vtx = ET.SubElement(vertices,'vertex')
            coord = ET.SubElement(vtx,'coordinates')
            x = ET.SubElement(coord,'x')
            x.text = str(v.x)
            y = ET.SubElement(coord,'y')
            y.text = str(v.y)
            z = ET.SubElement(coord,'z')
            z.text = str(v.z)

        #add triangles
        for t in self.mesh.triangles:
            triangle = ET.SubElement(volume,'triangle')
            v1 = ET.SubElement(triangle,'v1')
            v1.text = str(t[0])
            v2 = ET.SubElement(triangle,'v2')
            v2.text = str(t[1])
            v3 = ET.SubElement(triangle,'v3')
            v3.text = str(t[2])


        ET.ElementTree(amf).write(outFile,encoding='ISO-8859-1')

        
JSON_TEMPLATE= """\
{
    "metadata" :
    {
        "formatVersion" : 3,
        "generatedBy"   : "ParametricParts",
        "vertices"      : %(nVertices)d,
        "faces"         : %(nFaces)d,
        "normals"       : 0,
        "colors"        : 0,
        "uvs"           : 0,
        "materials"     : 1,
        "morphTargets"  : 0
    },

    "scale" : 1.0,

    "materials": [    {
    "DbgColor" : 15658734,
    "DbgIndex" : 0,
    "DbgName" : "Material",
    "colorAmbient" : [0.0, 0.0, 0.0],
    "colorDiffuse" : [0.6400000190734865, 0.10179081114814892, 0.126246120426746],
    "colorSpecular" : [0.5, 0.5, 0.5],
    "shading" : "Lambert",
    "specularCoef" : 50,
    "transparency" : 1.0,
    "vertexColors" : false
    }],

    "vertices": %(vertices)s,

    "morphTargets": [],

    "normals": [],

    "colors": [],

    "uvs": [[]],

    "faces": %(faces)s
}
"""        