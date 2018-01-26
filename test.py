import cadquery as cq

# CadQuery code
result = cq.Workplane('XY').dxf('profile.dxf').extrude(30.0)
result.exportSvg("profile_3D.svg" )