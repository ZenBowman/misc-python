import random
import math
import matplotlib.pyplot as plt
from PolygonTypes import Point, Line, Triangle, Quadrilateral, Bounds

def draw_line(l, fmt):
    xs = (l.origin.x, l.end.x)
    ys = (l.origin.y, l.end.y)
    line, = plt.plot(xs, ys, fmt)
        
PolygonTypes = {
    "Quadrilateral": Quadrilateral,
    "Triangle": Triangle
    }

# Source = http://www.bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
	return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)

def intersect(A,B,C,D):
        return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def lines_intersect(l1, l2):
    return intersect(l1.origin, l1.end, l2.origin, l2.end)

def polygons_intersect(poly1, poly2):
    for i in range(len(poly1.lines)):
        for j in range(len(poly2.lines)):
            if lines_intersect(poly1.lines[i], poly2.lines[j]):
                return True
    return False

def is_valid_polygon(poly):
    for i in range(len(poly.lines)):
        for j in range(i, len(poly.lines)):
            if lines_intersect(poly.lines[i], poly.lines[j]):
                return False
    return True

def intersects_previous_polygons(polycandidate, polygons):
    for poly in polygons:
        if polygons_intersect(polycandidate, poly):
            return True
    return False

def create_polygon(bounds, polygons):
    # Creates a polygon within the specified bounding box
    polytype = random.randint(0, len(PolygonTypes)-1)
    polytype = PolygonTypes.keys()[polytype]
    while 1:
        polycandidate = PolygonTypes[polytype](bounds)
        if is_valid_polygon(polycandidate):
            if not intersects_previous_polygons(polycandidate, polygons):
                return polycandidate

def create_polygons(numpolygons, xmin, ymin, xmax, ymax):
    polygons = []
    bounds = Bounds(Point(xmin, ymin), Point(xmax, ymax))
    for i in range(numpolygons):
        polygons.append(create_polygon(bounds, polygons))
    return polygons
    
def draw_polygon(poly):
    for l in poly.sides():
        draw_line(l, 'r')

def draw_polygons(polys):
    plt.axis([-5,15,-5,15])
    for p in polys:
        draw_polygon(p)

def verts(poly):
    verts = set()
    for line in poly.sides():
        verts.add(line.origin)
        verts.add(line.end)
    return verts

def nonIntersectingLine(line, otherpolys):
    for poly in otherpolys:
        for l in poly.lines:
            if ((l.origin == line.end) or (l.end == line.end)):
                continue
            if lines_intersect(line, l):
                return False
    return True

def get_visible_verts_from_polygon(point, poly, otherpolys):
    vverts = set()
    polyverts = verts(poly)
    # find any vert such that the line from point to poly doesn't intersect an edge from another polygon
    for vert in polyverts:
        if nonIntersectingLine(Line(point, vert), otherpolys):
            vverts.add(vert)
    return vverts

def get_visible_verts(point, polys):
    visibleVerts = set()
    for poly in polys:
        visibleVerts.update(get_visible_verts_from_polygon(point, poly, polys))
    return visibleVerts

def draw_point(p, fmt):
    plt.plot((p.x), (p.y), fmt)

def getPercepts(robotPosition, polygons):
    percepts = []
    ps = get_visible_verts(robotPosition, polygons)
    for p in ps:
        pass


if __name__ == "__main__":
    ps = create_polygons(10,0,0,10,10)
    draw_polygons(ps)
    p = Point(-1,-1)
    draw_point(p, 'ro')
    ps = get_visible_verts(p, ps)
    for _p in ps:
        draw_point(_p, 'bo')
        draw_line(Line(p, _p), 'b--')
    plt.show()
