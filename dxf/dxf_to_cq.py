import read_dxf as rd
import cadquery as cq
from pointmap import *
from cadquery import *

def _dxf(self, src, forConstruction=False):
    """
    Create a 2D drawing from a DXF source, using lines, arcs, and circles
    :param src: dxf source file
    :type src: string indicating filepath/file.dxf
    :param forConstruction: whether or not the edges are used for reference
    :type forConstruction: true if the edges are for reference, false if they are for creating geometry
        part geometry
    :return: a new CQ object with the created wires on the stack
    """

    # Our list of new edges that will go into a new CQ object
    dwg = rd.import_drawing(src)

    wires = []

    #add edges
    for loop in dwg.get_loops()[0]:
        for e in loop:
            start = dwg.coordinates(e[0])
            end = dwg.coordinates(e[1])
            startPoint = self.plane.toWorldCoords((start[0], start[1]))
            endPoint = self.plane.toWorldCoords((end[0], end[1]))
            edgeData = dwg.edgeData(e)

            if edgeData == {}:
                line = Edge.makeLine(startPoint, endPoint)
                self._addPendingEdge(line)
            else:
                mid = edgeData['arc']
                midPoint = self.plane.toWorldCoords((mid[0], mid[1]))
                arc = Edge.makeThreePointArc(startPoint, midPoint, endPoint)
                self._addPendingEdge(arc)
        new_wire = self.wire()
        wires.append(new_wire)

    # add circles
    for c in dwg.circles:
        radius = c[1]
        center = Vector(c[0][0], c[0][1], 0)
        norm = Vector(0, 0, 1)
        circle = Wire.makeCircle(radius, center, norm)
        wires.append(circle)
        self.ctx.pendingWires.append(circle)

    return self.newObject(wires)

cq.Workplane.dxf = _dxf

# result = (cq.Workplane('XY')
#     .dxf('tests/rectangles.dxf')
#     .extrude(5)
#     .findSolid().exportStep('dxf_out_01.step')
# )