import cadquery as cq
from cadquery import selectors

# This exemple demonstrates the use of a fillet to reinforce a junction between two parts.
# It relies on the selection of an edge of the weak junction, and the use of fillet.

# 1 - The construction of the model : a pipe connector
# In that model, the junction surface between the box and the cylinder is small.
# This makes the junction between the two too weak.
model = cq.Workplane("XY").box(15.0, 15.0, 2.0)\
    .faces(">Z").rect(10.0, 10.0, forConstruction=True)\
    .vertices().cskHole(2.0, 4.0, 82)\
    .faces(">Z").circle(4.0).extrude(10.0)\
    .faces(">Z").hole(6)

# 2 - Reinforcement of the junction
# Two steps here :
#  - select the edge to reinforce. Here we search the closest edge from the center on the top face of the box.
#  - apply a fillet or a chamfer to that edge
result = model.faces('<Z[1]').edges(selectors.NearestToPointSelector((0.0, 0.0))).fillet(1)

# Additional note :
# Using a type selector to select circles on the face would have returned all the circles, including the one to reinforce,
# but also the ones for the countersunk holes.
# The order of the edges returned by the selector is not guaranteed, so selecting the circle in the stack would not be reliable.
# If there was only one circle on the face, then this would have worked perfectly :
# result = model.faces('<Z[1]').edges('%Circle').fillet(1)

show_object(result)
