# ---------------------------------------
# n-simplex
# ---------------------------------------
# :id      -- has to be ordered tuple
# :n       -- n-simplex
# :facets  -- set of (n-1) faces
# :cofaces -- set of (n+1) faces
class Simplex:
    def __init__(self, id):
        # basic properties
        self.id = id
        self.n = len(id)-1
        self.facets = set()
        self.cofaces = set()

        # additional properties
        # (bad design in terms of generality, but more performant, than making wrappers)
        self.Q = 0
        self.error = 0
        self.heap_index = -1
        self.c = None
    
    # neighbors of simplex with same dimension
    def get_neighbours(self):
        return set.union(*[s.cofaces for s in self.facets]).difference({self})
    
    # not optmizied but is in constant time relative to the size of the triangulation
    def update_id(self):
        if self.n == 0:
            return set(self.id)
        # recursively update ids of facets
        id = set.union(*[s.update_id() for s in self.facets])
        self.id = tuple(sorted(id))
        return id
    
    # link of vertex v (0 and 1-simplexes)
    # (-> we could probbably only check if there are any 1-simplexes in the vertex link for the lemma?)
    def vertex_link(self):
        es = self.cofaces
        ts = set.union(*[s.cofaces for s in es])
        # 1-skeleton
        skel1 = set.union(*[t.facets for t in ts])
        # 0-skeleton
        skel0 = set.union(*[s.facets for s in skel1])
        s1 = skel1.difference(es)
        s0 = skel0.difference({self})
        return s1.union(s0)
    
    # link of edge e (only 0-simplexes)
    def edge_link(self):
        ts = self.cofaces
        # 0-skeleton
        skel = set.union(*[t.facets for t in ts])
        skel = set.union(*[s.facets for s in skel])
        vs = self.facets
        return skel.difference(vs)
    
    # link of simplex s
    def link(self):
        if self.n == 0:
            return self.vertex_link()
        elif self.n == 1:
            return self.edge_link()
        elif self.n == 2:
            return {self}