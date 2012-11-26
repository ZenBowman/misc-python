
class Vertex:
    def __init__(self, key):
        self.key = key
        self.adjlist = {}

    def display(self):
        print "Key = %s\tEdges = %s" % (self.key, str(self.adjlist.keys()))

    def __repr__(self):
        return "%s: %s" % (str(self.key), str(self.adjlist.keys()))

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, key):
        self.vertices[key] = Vertex(key)

    def add_directed_edge(self, fromv, tov, weight):
        self.vertices[fromv].adjlist[tov] = weight

    def add_undirected_edge(self, fromv, tov, weight):
        self.add_directed_edge(fromv, tov, weight)
        self.add_directed_edge(tov, fromv, weight)
        
    def create(self):
        print "Graph creation helper"
        directed = False
        directedq = raw_input("Is this a directed graph (y or n)?")
        if directedq.lower() == 'y':
            directed = True
        while 1:
            v = raw_input("Enter Vertex key, hit 'q' when finished:\t")
            if v=='q':
                break
            self.add_vertex(v)

        while 1:
            s = raw_input("Starting vertex ('q' to exit):\t")
            if (s == 'q'):
                break
            e = raw_input("Ending vertex:\t")
            if directed:
                self.add_directed_edge(s,e,1)
            else:
                self.add_undirected_edge(s,e,1)
                
    def display(self):
        for vert in self.vertices.values():
            vert.display()

    def dfs(self, vertex, target):
        visited = []
        self.vertices[vertex].d = 0
        queue = [self.vertices[vertex]]
        d = 0
        
        while len(queue) > 0:
            u = queue[0]
            visited.append(u)
            if u.key == target:
                return (u, d)
            queue = queue[1:]
            for v in u.adjlist.keys():
                vert = self.vertices[v]
                if ((vert not in visited) and (vert not in queue)):
                    print "Adding %s to queue" % vert
                    queue.append(vert)
            d += 1


if __name__ == "__main__":
    g = Graph()
    g.create()
    g.display()
    print g.dfs('1','3')
