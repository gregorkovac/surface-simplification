from Hasse import Hasse
from MaxHeap import MaxHeap

import numpy as np
from scipy.optimize import minimize

class Simplify:
    def __init__(self, path):
        self.path = path

        if path.endswith('.obj'):
            self.V, self.T = self.read_obj()
        elif path.endswith('.ply'):
            self.V, self.T = self.read_ply()

        self.hasse = Hasse(self.T)
        self.initialize_Q()
        self.initialize_error()
        self.heap = MaxHeap(self.hasse.F[1])

    def read_obj(self):
        with open(self.path) as f:
            lines = f.readlines()

        v_lines = [line for line in lines if line.startswith('v')]
        f_lines = [line for line in lines if line.startswith('f')]

        V = []
        T_id = []

        for line in v_lines:
            v = np.array([float(x) for x in line.split()[1:]], dtype=np.float32)
            V.append(v)
        
        for line in f_lines:
            t = [int(x)-1 for x in line.split()[1:]]
            t = tuple(sorted(t))
            T_id.append(t)

        return V, T_id
    
    def read_ply(self):
        with open(self.path, 'r') as f:
            lines = f.readlines()

        vertex_data_start = lines.index('end_header\n') + 1

        V = []
        T_id = []

        for i in range(vertex_data_start, len(lines)):
            line = lines[i].strip().split()
            if len(line) == 5:
                line = line[0:3]
                v = np.array([float(x) for x in line], dtype=np.float32)
                V.append(v)
            elif line[0] == '3':
                t = [int(x) for x in line[1:4]]
                t = tuple(sorted(t))
                if t not in T_id:
                    T_id.append(t)

        return V, T_id
    
    def abs2geo(self, T):
        return [(self.V[t[0]], self.V[t[1]], self.V[t[2]]) for t in T if len(t) == 3]
    
    # check if the contraction of e doesn't change the topology type of the triangulation
    # -> check if it's safe to contract edge e
    @staticmethod
    def is_safe(e):
        return e.link() == set.intersection(*[v.link() for v in e.facets])

    # compute quadric for triangle t
    def compute_Q(self, t):
        a, b, c = [self.V[v] for v in t.id]

        normal = np.cross(b - a, c - a)
        normal = normal / np.linalg.norm(normal)

        offset = -np.dot(normal, a)

        u = np.array([*normal, offset])

        return np.outer(u, u)

    # initialize quadrics for all simplices
    def initialize_Q(self):
        for t in self.hasse.F[2]:
            t.Q = self.compute_Q(t)
        for e in self.hasse.F[1]:
            e.Q = np.sum([t.Q for t in e.cofaces], axis=0)
        for v in self.hasse.F[0]:
            v.Q = np.sum([t.Q for t in set.union(*[e.cofaces for e in v.cofaces])], axis=0)

    @staticmethod  
    def compute_E_H(x, Q):
        x = np.array([*x, 1])
        return np.dot(np.dot(x, Q), x)

    def compute_error(self, e):
        a, b = [self.V[v] for v in e.id]
        initial_guess = (a + b) / 2
        Q = e.Q
        #Q = np.sum([v.Q for v in e.facets], axis=0) - e.Q
        c = minimize(self.compute_E_H, initial_guess, args=(Q)).x
        #c = np.array([1,1,1])
        e.c = c

        return self.compute_E_H(c, Q)
    
    def initialize_error(self):
        for e in self.hasse.F[1]:
            e.error = self.compute_error(e)

    def contract_edge(self, e):
        # contract edge e in the diagram structure
        v0, v1, e10, e11 = self.hasse.contract_edge(e)

        # remove from heap the two additional edges that were removed from the diagram
        # if they haven't yet been removed
        # (an edge might have been removed if it was unsafe to contract)
        if e10 in self.heap:
            self.heap.remove(e10)
        if e11 in self.heap:
            self.heap.remove(e11)
        
        # e.c.Q = e.facets[0].Q + e.facets[1].Q - e.Q
        # e.c.cofaces[0].Q = 
        # self.initialize_error()

        # update the position of the "new" verex
        # (the vertex that was created by contracting edge e)
        # (-- Not actually new, just overwritten)
        self.V[v0.id[0]] = e.c

    # simplify the triangulation n times
    # if n is negative, simplify until the triangulation is minimal
    # (might be useful for looking at the 'filtrarion')
    def simplify(self, n=-1):
        count = 0
        while len(self.heap) > 0 and count != n:            
            e = self.heap.pop()
            #print(e.heap_index, len(self.heap), ' : F')

            if self.is_safe(e):
                self.contract_edge(e)
                count += 1
            else:
                pass
                #print("Not safe", e.heap_index, len(self.heap))

        return [t.id for t in self.hasse.F[2]]