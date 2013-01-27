import random
import math
import matplotlib.pyplot as plt

MINEDGESIZE = 0.75
MAXEDGESIZE = 2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def squaredDistance(self, other):
        return (self.x-other.x)**2 + (self.y-other.y)**2

def pointToLineDistance(a, b, p):
    normalLength = math.hypot(b.x - a.x, b.y - a.y);
    return abs((p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x)) / normalLength;


def createPointWithinBounds(bounds):
    return Point(random.uniform(bounds.bottomLeft.x, bounds.topRight.x), random.uniform(bounds.bottomLeft.y, bounds.topRight.y))

def createPointWithinRange(point, mindistance, maxdistance):
    xopt1 = random.uniform(point.x-maxdistance, point.x-mindistance)
    xopt2 = random.uniform(point.x+mindistance, point.x+maxdistance)
    yopt1 = random.uniform(point.y-mindistance, point.y-mindistance)
    yopt2 = random.uniform(point.y+mindistance, point.y+maxdistance)

    xr = random.choice([1,2])
    xval = xopt1
    if xr == 2:
        xval = xopt2
        
    yr = random.choice([1,2])
    yval = yopt1
    if yr == 2:
        yval = yopt2
    return Point( xval, yval )

class Line:
    def __init__(self, origin, end):
        self.origin = origin
        self.end = end

def draw_line(l, fmt):
    xs = (l.origin.x, l.end.x)
    ys = (l.origin.y, l.end.y)
    line, = plt.plot(xs, ys, fmt)
        
class Bounds:
    def __init__(self, bottomLeft, topRight):
        self.bottomLeft = bottomLeft
        self.topRight = topRight

class Polygon:
    def sides(self):
        raise Exception("Not implemented!")

class Triangle:
    def __init__(self, bounds):
        #print "Creating triangle"
        self.lines = []
        p1 = createPointWithinBounds(bounds)
        p2 = createPointWithinRange(p1, MINEDGESIZE, MAXEDGESIZE)
        p3 = createPointWithinRange(p2, MINEDGESIZE, MAXEDGESIZE)
        self.lines.append(Line(p1, p2))
        self.lines.append(Line(p2, p3))
        self.lines.append(Line(p3, p1))
        
    def sides(self):
        return self.lines
        
def lineClosestToPoint(lines, point):
    mindist = 9999
    index = -1
    for i in range(len(lines)):
        l = lines[i]
        dist = pointToLineDistance(l.origin, l.end, point)
        if dist < mindist:
            dist = mindist
            index = i
    return i, lines[i]

class Quadrilateral:
    def __init__(self, bounds):
        #print "Creating quadrilateral"
        self.lines = []
        p1 = createPointWithinBounds(bounds)
        p2 = createPointWithinRange(p1, MINEDGESIZE, MAXEDGESIZE)
        p3 = createPointWithinRange(p2, MINEDGESIZE, MAXEDGESIZE)
        p4 = createPointWithinRange(p3, MINEDGESIZE, MAXEDGESIZE)
        tempLines = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]
        closestLineIndex, closestLine = lineClosestToPoint(tempLines, p4)
        tempLines.pop(closestLineIndex)
        l3 = Line(closestLine.origin, p4)
        l4 = Line(closestLine.end, p4)
        self.lines = tempLines
        self.lines.append(l3)
        self.lines.append(l4)


    def sides(self):
        return self.lines

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

if __name__ == "__main__":
    ps = create_polygons(10,0,0,10,10)
    draw_polygons(ps)
    p = Point(1,1)
    draw_point(p, 'ro')
    ps = get_visible_verts(p, ps)
    for _p in ps:
        draw_point(_p, 'bo')
        draw_line(Line(p, _p), 'b--')
    plt.show()
