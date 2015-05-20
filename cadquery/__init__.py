import os

selectedAPI = os.environ.get("CADQUERYAPI")

if selectedAPI is None or selectedAPI.upper() == 'FREECAD':
    # These items point to the FreeCAD implementation
    from .freecad_impl.geom import Plane, BoundBox, Vector, Matrix, sortWiresByBuildOrder
    from .freecad_impl.shapes import Shape, Vertex, Edge, Face, Wire, Solid, Shell, Compound
    from .freecad_impl import exporters
    from .freecad_impl import importers
else:
    from .pythonocc_impl.geom import Vector, Matrix, Plane

# These items are the common implementation
# The order of these matter
# from .selectors import NearestToPointSelector,ParallelDirSelector,DirectionSelector,PerpendicularDirSelector,TypeSelector,DirectionMinMaxSelector,StringSyntaxSelector,Selector
# from .CQ import CQ,CQContext,Workplane


__all__ = [
    'CQ', 'Workplane', 'plugins', 'selectors', 'Plane', 'BoundBox', 'Matrix', 'Vector', 'sortWiresByBuildOrder',
    'Shape', 'Vertex', 'Edge', 'Wire', 'Solid', 'Shell', 'Compound', 'exporters', 'importers', 'NearestToPointSelector', 'ParallelDirSelector', 'DirectionSelector', 'PerpendicularDirSelector', 'TypeSelector', 'DirectionMinMaxSelector', 'StringSyntaxSelector', 'Selector', 'plugins'
]

__version__ = "0.1.8"
