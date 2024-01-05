from Simplex import Simplex
from itertools import combinations

def gen_facets_id(s):
    return list(combinations(s.id, s.n))

# class for constructing and storing hasse diagram
class Hasse:
    def __init__(self, T):
        self.F = [dict() for i in range(len(T[0]))]
        for s_id in T:
            s = Simplex(s_id)
            self.F[-1][s_id] = s
            self.__hasse(s)
        for i, f in enumerate(self.F):
            self.F[i] = list(f.values())

    def __hasse(self, s):
        if s.n == 0:
            return
        E_id = gen_facets_id(s)
        A = self.F[s.n-1]
        for e in E_id:
            if e not in A:
                A[e] = Simplex(e)
        E = {A[e] for e in E_id}
        s.facets = {e for e in E}
        for e in E:
            e.cofaces.add(s)
        for e in E:
            self.__hasse(e)

    # remove simplex s from the diagram
    def remove_simplex(self, s):
        for e in s.facets:
            if s in e.cofaces:
                e.cofaces.remove(s)
        for e in s.cofaces:
            if s in e.facets:
                e.facets.remove(s)
        self.F[s.n].remove(s)

    # replace simplex s1 with simplex s2 (only for cofaces)
    def replace(self, s1, s2):
        cofaces = list(s1.cofaces)
        for e in cofaces:
            e.facets.remove(s1)
            e.facets.add(s2)
            s2.cofaces.add(e)

    # contract edge
    # e -- 1-simplex
    def contract_edge(self, e):
        # triangles with edge e (always 2)
        ts = list(e.cofaces)
        t0 = ts[0]
        t1 = ts[1]

        # vertices of edge
        vs = list(e.facets)
        v0 = vs[0]
        v1 = vs[1]

        # edges that are part of the hole
        e0 = v0.cofaces.difference({e})
        e1 = v1.cofaces.difference({e})
        e00 = e0.intersection(t0.facets).pop()
        e01 = e0.intersection(t1.facets).pop()
        e10 = e1.intersection(t0.facets).pop()
        e11 = e1.intersection(t1.facets).pop()

        # replace edges
        self.replace(e10, e00)
        self.replace(e11, e01)

        # replace vertex v1 with v0
        self.replace(v1, v0)

        # remove the edge
        self.remove_simplex(e)

        # remove both triangles
        self.remove_simplex(t0)
        self.remove_simplex(t1)        

        # remove one point
        self.remove_simplex(v1)

        # remove the two edges
        self.remove_simplex(e10)
        self.remove_simplex(e11)

        # update ids around v0
        # get all neighbouring triangles
        tris = set.union(*[edge.cofaces for edge in set.union(v0.cofaces)])
        for t in tris:
            t.update_id()
        return v0, v1, e00, e01, e10, e11, t0, t1
            
    def get_all_simplices(self):
        all_simplices = set()
        for f in self.F:
            all_simplices = all_simplices.union(f)
            
        all_simplices = [s.id for s in all_simplices]

        return all_simplices