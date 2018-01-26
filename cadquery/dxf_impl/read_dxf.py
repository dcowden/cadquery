import ezdxf
import sys
import logging
from pointmap import EntityMap
from vec2d import Vec2d

log = logging.getLogger('generate')
#
# Reads a DXF, and creates Onshape FS code that will produce that value.
# DXF import in Onshape is really horrible!
#z

#TODO: factor out precision. very important to eliminate rounding error!

"""
 lookup table template.
 the top selection is always called 'category'

 there can be any other number of levels in the middle, including zero.

 The root folder is mapped to the 'Category' choice.

 Each level is of the tree is scanned for sub-folders that contain files.
 If they exist, a selection named 'Profile' is generated, with each
 selection matching a file

 Each intermediate path is matched using the default template.
 Directories that match the template have its selection name used from the template

 In each case, the first entry in the list is set to the default value
"""
DXF_UNIT_XREF={
	0: 'inch',
	1: 'inch',
	2: 'feet',
	3: 'miles',
	4: 'millimeter',
	5: 'cm',
	6: 'm',
	7: 'km'
}

def compute_arc_points(center_point_tuple, radius, startAngle, endAngle ):
	#given center point, radius, and start/end angles, produce
	#three points for use in a 3 point arc
	center= Vec2d(center_point_tuple)

	angle_diff = endAngle - startAngle
	if angle_diff < 0:
		angle_diff = angle_diff + 360.0
	mid_angle = startAngle  +  (angle_diff / 2.0)
	#log.debug("Angles=%d,%d,%d"% (startAngle,endAngle,mid_angle))
	start_point =   center + (Vec2d(radius,0).rotated(startAngle))
	end_point = center + ( Vec2d(radius,0).rotated(endAngle))
	mid_point = center + ( Vec2d(radius,0).rotated(mid_angle))
	return ( (start_point.x,start_point.y),(mid_point.x,mid_point.y),(end_point.x,end_point.y))

def import_drawing(filePath ,function_name="make_shape",reCenter=True):
	"""
		Creates a featurescript version of a DXF.

		There are a few requirements
			Use a little space as possible
			check points to avoid non-closed curves.

		Limitiation:
			We ignore the z direction completely.
			We rely on some externally defined functions, so that we can keep the text very, very short
			Sometimes drawings have no values for INSUNITS-- not sure what to do there

	"""
	log = logging.getLogger("import_drawing")

	log.info ("Converting Drawing %s " % filePath)
	dxf = ezdxf.readfile(filePath)

	m = dxf.modelspace()

	drawing_uom = 'inch'
	insunits = None
	try:
		insunits = dxf.header['$INSUNITS']
	except:
		pass
	if insunits != None and DXF_UNIT_XREF.has_key(insunits):
		drawing_uom = DXF_UNIT_XREF[dxf.header['$INSUNITS']]

	entityMap = EntityMap(tolerance=0.001, uom=drawing_uom, function_name=function_name,numberFormat="%0.5f")
	def makePolyLine(point1,point2):
		log.debug("Processing DXF Polyline Entity %s -> %s " % ( str(point1), str(point2) ) )
		if point1[4] != 0.0:
			midpoint = compute_arc_midpoint(point1,point2)
			entityMap.arc(point1[:2],midpoint[:2],point2[:2])
		else:
			entityMap.line(point1[:2],point2[:2])

	for entity in m:
		if entity.dxftype() == 'LWPOLYLINE':

			points = list(entity.get_points())
			for idx,point in enumerate(points[:-1]):
				nextpoint = points[idx+1]
				makePolyLine(point,nextpoint)

			if entity.closed:
				makePolyLine(points[-1],points[0])
		elif entity.dxftype() == 'LINE':
			log.debug("Processing DXF LINE: %s -> %s " % ( str(entity.dxf.start), str(entity.dxf.end )) )
			entityMap.line(entity.dxf.start[:2], entity.dxf.end[:2] )
		elif entity.dxftype() == 'ARC':
			log.debug("Processing DXF ARC: center=%s ,radius %s " % ( str(entity.dxf.center), str(entity.dxf.radius) ) )
			(start,mid,end) = compute_arc_points(entity.dxf.center,entity.dxf.radius,entity.dxf.start_angle,entity.dxf.end_angle)
			log.debug("Processing DXF ARC: start=%s ,mid= %s, end= %s " % ( str(start), str(mid),str(end) ) )
			entityMap.arc(start[:2],mid[:2],end[:2])
		elif entity.dxftype() == 'CIRCLE':
			entityMap.circle((entity.dxf.center,entity.dxf.radius))
		elif entity.dxftype() == 'TEXT':
			log.info("Skipping Text entity")
		else:
			raise ValueError("Unhandled DXF entity type '%s' in drawing '%s'" % ( entity.dxftype(), filePath ) )

	log.debug ("EntityMap"+str(entityMap))

	if reCenter:
		log.info("Re-Centering ...")
		entityMap = entityMap.centered()
	return entityMap

def compute_arc_midpoint(point1, point2 ):
	"""
		computes the middle point of an arc between two points,
		where the geometry was specified using the autocad LWPolyline 'bulge' value.
	"""
	log.debug("Point1=",point1,"point2=",point2)
	p1 = Vec2d( point1[0], point1[1] )
	p2 = Vec2d( point2[0], point2[1] )
	bulge = point1[4]
	distance = p1.get_distance(p2)
	radius = distance / 2.0 * abs(bulge)
	midpoint = (p1 + p2 ) / 2.0

	multiplier = 1.0
	if bulge < 0:
		multiplier = -1.0

	perp = (p1 - p2).perpendicular_normal() * multiplier

	arcpoint = midpoint + (radius)* perp
	log.debug ( "Distance=%s,Radius=%s,Midpoint=%s,perp=%s,bulge=%s,arcpoint=%s" %  ( str(distance), str(radius), str(midpoint), str(perp), str(bulge) , str(arcpoint) )  )
	return ( arcpoint.x, arcpoint.y )