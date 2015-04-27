"""
    Copyright (C) 2011-2015  Parametric Products Intellectual Holdings, LLC

    This file is part of CadQuery.

    CadQuery is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    CadQuery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; If not, see <http://www.gnu.org/licenses/>
"""
import cadquery
import OCC.Geom.Geom_Vector as OCCVector

def sortWiresByBuildOrder(wireList, plane, result=[]):
    """
        Tries to determine how wires should be combined into faces.
        Assume:
            The wires make up one or more faces, which could have 'holes'
            Outer wires are listed ahead of inner wires
            there are no wires inside wires inside wires ( IE, islands -- we can deal with that later on )
            none of the wires are construction wires
        Compute:
            one or more sets of wires, with the outer wire listed first, and inner ones
        Returns, list of lists.
    """

    remainingWires = list(wireList)
    while remainingWires:
        outerWire = remainingWires.pop(0)
        group = [outerWire]
        otherWires = list(remainingWires)
        for w in otherWires:
            if plane.isWireInside(outerWire, w):
                group.append(w)
                remainingWires.remove(w)
        result.append(group)

    return result


class Vector(object):
    """
        Create a 3-dimensional vector

        :param *args: a 3-d vector, with x-y-z parts.

        you can either provide:
            * a PythonOCC vector
            * a vector ( in which case it is copied )
            * a 3-tuple
            * three float values, x, y, and z

        This vector is immutable-- all mutations return a copy!
    """

    def __init__(self, *args):
        if len(args) == 3:
            #TODO: We've been given separate X, Y and Z values, convert to PythonOCC vector
            pass
        elif len(args) == 1:
            if type(args[0]) is tuple:
                #TODO: We've been given a tuple, convert to PythonOCC vector
                pass
            elif type(args[0] is OCCVector):
                #TODO: Fix this, we've been given a PythonOCC vector
                pass
            elif type(args[0] is Vector):
                fV = args[0].wrapped
            else:
                fV = args[0]
        else:
            raise ValueError("Expected three floats, PythonOCC vector, or 3-tuple")

        self.wrapped = fV
        self.Length = fV.Length
        self.x = fV.x
        self.y = fV.y
        self.z = fV.z