import cadquery as cq

r = cq.Workplane('XY').dxf('cadquery/plugins/dxf/tests/1515-ULS.dxf').extrude(5)