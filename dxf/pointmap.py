import string
import math
import networkx as nx

import logging

BIG_NUMBER = 1e30

log = logging.getLogger('pointmap')

def subtract2d( coord1, coord2 ):
	return (  coord1[0] - coord2[0], coord1[1] - coord2[1])


class BoundingBox2D(object):
	def __init__(self):
		self.minVal = ( BIG_NUMBER, BIG_NUMBER )
		self.maxVal = ( -BIG_NUMBER, -BIG_NUMBER)

	def acceptNode(self, coordinate2D):
		self.minVal = ( min (self.minVal[0],coordinate2D[0]), min(self.minVal[1],coordinate2D[1]) )
		self.maxVal = ( max (self.maxVal[0],coordinate2D[0]), max(self.maxVal[1],coordinate2D[1]) )
		#print "min=%s, max=%s, input=%s" % (self.minVal, self.maxVal, coordinate2D )
	def acceptCircle(self,center2D, radius):
		self.acceptNode( (center2D[0] + radius, center2D[1] + radius  ) )
		self.acceptNode( (center2D[0] - radius, center2D[1] - radius  ) )

	def getMin(self):
		return self.minVal

	def getMax(self):
		return self.maxVal

	def getCenter(self):
		size = subtract2d ( self.maxVal, self.minVal )
		return (  self.minVal[0] + (size[0]/2.0), self.minVal[1] + (size[1]/2.0)  )

class EntityMap(object):
	"""
		represents a dxf drawing, where each point refers to a named point, rather than a numeric value.

		This is an internal representation, that reprsents everything as a line or a 3 point arc.
		DXF can refer to a polyline, which is converted to 3point arcs and lines.
		These forms are used because they specify end points, which can be tolerance checked.

		Internally, the points are compared to others available, and are 'snapped' to existing ones

	"""
	ARC = 'ARC'
	LINE='LINE'
	COORD_KEY='coords'
	ARC_POINT_KEY='arc'
	def __init__(self, tolerance=0.00001, uom="inch",function_name="make_shape",numberFormat="%0.3f"):
		self.nodeCounter = 0
		self.g = nx.Graph()  #each node is a point. each edge is an edge
		self.tolerance=tolerance
		self.uom = uom
		self.numberFormat = numberFormat
		self.function_name = function_name
		self.circles = []

	def arc ( self, start, mid, end ):
		"""
			Add an arc. start, mid, and end are xy-tuples
		"""
		if len(start) != 2 or len(mid) != 2 or len(end) !=2:
			raise ValueError("Expected Tuples for start,mid, end")
		s = self._get_node(start)
		e = self._get_node(end)

		self.g.add_edge(s,e,{EntityMap.ARC_POINT_KEY: mid } )
		log.debug ("Added Arc %d->%d via %s" % (s,e,str(mid)))

	def line ( self, start, end ):
		"""
			Add a line. start and end are node ids
		"""
		if len(start) != 2 or len(end) !=2:
			raise ValueError("Expected Tuples for start,mid, end")
		s = self._get_node(start)
		e = self._get_node(end)
		log.debug( "Adding Edge %d->%d" % ( s, e))
		self.g.add_edge(s,e, {} )

	def nodeData(self,nodeId):
		return self.g.node[nodeId]

	def coordinates(self,nodeId):
		return self.g.node[nodeId]["coords"]

	def edgeData(self,edgeTuple):
		return self.g.edge[edgeTuple[0]][edgeTuple[1]]

	def circle(self, circle ):
		# a circle is  ( (x,y), radius )
		self.circles.append(circle)

	def get_circles(self):
		#TODO: this seems like a hack. will each entity type have its own thing?
		return self.circles

	def get_loops(self):
		"""
			Gets all of the loops in the drawing
			they are returned with node references only

			we should never have graphs with nodes left over
			but if we do, we'll raise a warning. it probably means
			that shape will not work right when extruded, because it will
			have an open contour
			returns a tuple:
			  ( listOfCycles, nodesLeftOver )
		"""
		log.debug( "Finding Cycles. Graph="+str(self) )
		tmp_graph = self.g.copy()
		cycles = []
		while len(tmp_graph.edges() ) > 0:
			try:
				cycle = nx.find_cycle(tmp_graph)
				if len(cycle) > 0:
					log.debug("Found loop: " + str(cycle))
					cycles.append(cycle)
				tmp_graph.remove_edges_from(cycle)
			except:
				#no cycles found. open contour
				log.warn("Exception Finding Loop Cycles")
				#print 'WARNING: This graph has nodes not connected with a loop. It probably has open contours!!'
				break;
		log.debug("JustBeforeturn, remaining graph looks like this");
		log.debug(tmp_graph.edges())

		return ( cycles, tmp_graph.edges() )

	def formatTemplate(self,templateText):
		return templateText.replace("#NUM#",self.numberFormat)

	def _get_node(self,xytuple):
		#creates a node if necessary, trying to re-use existing nodes within tolerance
		n = self.find_node(xytuple)
		if n is not None:
			#print "Re-use Node",n
			return n
		else:
			nodeVal = {EntityMap.COORD_KEY: xytuple}
			nodeId = self.nodeCounter
			log.debug ( "Add Node %d : (%0.3f,%0.3f)" % (nodeId, xytuple[0],xytuple[1] ))
			self.g.add_node(nodeId,nodeVal)
			self.nodeCounter += 1
			return nodeId

	def find_node(self, xytuple):
		#finds an existing node having the same x-y coordinate, within tolerance, or none if not found
		for n in self.g.nodes(data=True):
			coord = n[1][EntityMap.COORD_KEY]
			if self.points_are_equal(xytuple, coord ):
				log.debug( "%s looks like existing node %d %s " % ( str(xytuple), n[0], str(coord) ) )
				return n[0]

		return None

	#check to see if two points are within a given distance of each other
	def points_are_equal (self, point1, point2 ):
		#log.debug ( "Checking Distance" + str(point1)+ str(point2) )
		d = math.hypot(point2[0] - point1[0], point2[1] - point1[1] )
		return d < self.tolerance

	def centered (self ):
		"""
			returns a version of this map transformed so that it is centered around the origin.
			TODO: it would really be better to use the underlying
			nodes and edges rather than re-creating this, for performance reasons.
		"""

		box = BoundingBox2D()

		for n in self.g.nodes():
			coords = self.coordinates(n)
			box.acceptNode(coords)

		for c in self.circles:
			box.acceptCircle( c[0], c[1] )


		newCenter = box.getCenter()
		print ("newCenter = %s" % str(newCenter))
		centered = EntityMap(tolerance=self.tolerance, uom=self.uom,function_name=self.function_name,numberFormat=self.numberFormat )

		#add edges
		for e in self.g.edges():
			start = self.coordinates(e[0])
			end = self.coordinates(e[1])
			edgeData = self.edgeData(e)

			if edgeData == {}:
				centered.line( subtract2d(start ,newCenter),subtract2d( end , newCenter))
			else:
				mid = edgeData[EntityMap.ARC_POINT_KEY]
				centered.arc( subtract2d(start , newCenter), subtract2d(mid , newCenter), subtract2d(end , newCenter))

		#add circles
		for c in self.circles:
			centered.circle(  ( subtract2d(c[0],newCenter), c[1])  )

		return centered
	def __str__ ( self ):
		return "EntityMap:\n\t%d Nodes: %s\n\t%d Edges: %s \n\t%d Circles: %s " % (  len(self.g.nodes()) ,str(self.g.nodes(data=True)), len(self.g.edges()), str(self.g.edges(data=True)), len(self.circles), str(self.circles) )



def testEntityMapLines():
	e = EntityMap(tolerance=0.001)
	e.line((0,0),(1.0,0))
	e.line((1.0,0),(1.0,1.0))
	e.line((1.00004,1.0),(0.000004,1.000))
	e.line((0,1.000023433),(0.0,0.0))
	print e.get_loops()
	assert ([[(0,1),(1,2),(2,3),(3,0)]],[]   ) == e.get_loops()

def testMapWithDanglingEdges():
	e = EntityMap(tolerance=0.001)
	e.line((0,0),(1.0,0))
	e.line((1.0,0),(1.0,1.0))
	e.line((1.00004,1.0),(0.000004,1.000))
	e.line((0,1.000023433),(0.0,0.0))
	e.line((2.0,2.0),(3.0,3.0))  #this is a dangling edge, nodes 4 and 5
	assert ([[(0,1),(1,2),(2,3),(3,0)]],[(4,5)]   ) == e.get_loops()

def testTwoLoops():
	e = EntityMap(tolerance=0.001)
	e.line((0,0),(1.0,0))
	e.line((1.0,0),(1.0,1.0))
	e.line((1.00004,1.0),(0.000004,1.000))
	e.line((0,1.000023433),(0.0,0.0))
	e.line((2.0,2.0),(3.0,3.0))
	e.line((3.0,3.0004),(4.0,4.0))
	e.line((4.0,4.0),(2.0,2.0))
	assert ([[(0,1),(1,2),(2,3),(3,0)],[(4,5),(5,6),(6,4)] ],[]   ) == e.get_loops()

def testCentering():
	e = EntityMap(tolerance=0.001)

	e.line((0,0),(1.0,0))
	e.circle( (( 1.0,1.0 ), 1.0) )
	e.line((-1,-1),(-2,-1) )
	print str(e)

	c = e.centered()
	print str(c)

if __name__ == '__main__':
	print "Running Tests..."
	testEntityMapLines()
	testMapWithDanglingEdges()
	testTwoLoops()
	testCentering()
