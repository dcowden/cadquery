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
    :type forConstruction: true if edges are for reference, false if they are for creating geometry
        part geometry
    :return: a new CQ object with the created wires on the stack
    """

    # Our list of new edges that will go into a new CQ object
    dwg = rd.import_drawing(src)

    def findWindDirection(loop):
        score = 0
        for e in loop:
            start = dwg.coordinates(e[0])
            end = dwg.coordinates(e[1])

            score += (end[0] - start[0])*(end[1] + start[1])

        if score > 0:
            winding = 'CW'
        else:
            winding = 'CCW'
        return winding

    #add edges
    wires = []
    for loop in dwg.get_loops()[0]:
        edges = []
        winding = findWindDirection(loop)
        for e in loop:
            if winding is 'CW':
                start = dwg.coordinates(e[1])
                end = dwg.coordinates(e[0])
            else:
                start = dwg.coordinates(e[0])
                end = dwg.coordinates(e[1])
            startPoint = self.plane.toWorldCoords((start[0], start[1]))
            endPoint = self.plane.toWorldCoords((end[0], end[1]))
            edgeData = dwg.edgeData(e)

            # if startPoint is not endPoint:
            if edgeData == {}:
                line = Edge.makeLine(startPoint, endPoint)
                edges.append(line)
            else:
                mid = edgeData['arc']
                midPoint = self.plane.toWorldCoords((mid[0], mid[1]))
                arc = Edge.makeThreePointArc(startPoint, midPoint, endPoint)
                edges.append(arc)
        new_wire = Wire.assembleEdges(edges)
        wires.append(new_wire)

    for wire in wires:
        self.ctx.pendingWires.append(wire)

    # add circles
    for c in dwg.circles:
        radius = c[1]
        center = Vector(c[0][0], c[0][1], 0)
        norm = Vector(0, 0, 1)
        circle = Wire.makeCircle(radius, center, norm)
        wires.append(circle)
        self.ctx.pendingWires.append(circle)

    sorted_wires = sortWiresByBuildOrder(list(self.ctx.pendingWires), self.plane, [])

    sorted_wires.reverse()

    self.ctx.pendingWires = []

    for wirelist in sorted_wires:
        for wire in wirelist:
            self._addPendingWire(wire)

    return self.newObject(wires)

# register the dxf function to cq.
cq.Workplane.dxf = _dxf

def testDxf():
    r = cq.Workplane('XY').dxf('tests/1515-ULS.dxf').extrude(5)
    assert r.faces().size() == 194

if __name__ == '__main__':
    testDxf()