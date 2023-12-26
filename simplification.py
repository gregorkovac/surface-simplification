import matplotlib.pyplot as plt
import numpy as np

'''
compute_Q(T) returns the fundamental quadratic matrix of the function E_H(x) used for error calculation.
'''
def compute_Q(T):
    # TODO: Check if this is correct
    Q = np.zeros((4, 4))

    for t in T:
        a, b, x = t[0], t[1], t[2]

        v1 = np.array(b) - np.array(a)
        v2 = np.array(x) - np.array(a)

        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)

        offset = np.dot(normal, np.array(a))

        u = np.array([normal[0], normal[1], normal[2], offset])

        Q += np.outer(u, u.T)

    return Q

'''
compute_E_H(x) returns of the value of the E_H(x) function at point x = (x1, x2, x3). It also takes triangulation T as input.
'''
def compute_E_H(T, x, Q):
    # TODO: Check if this is correct
    x1, x2, x3 = x[0], x[1], x[2]

    A = Q[0, 0]
    P = Q[0, 1]
    q = Q[0, 2]
    U = Q[0, 3]
    B = Q[1, 1]
    R = Q[1, 2]
    V = Q[1, 3]
    C = Q[2, 2]
    W = Q[2, 3]
    Z = Q[3, 3]

    return A * x1 ** 2 + B * x2 ** 2 + C * x3 ** 2 + 2 * (P * x1 * x2 + Q * x1 * x3 + R * x2 * x3) + 2 * (U * x1 + V * x2 + W * x3) + Z
'''
error(T, e) returns the damage caused to the triangulation T by contracting the edge e = [(x1, y1), (x2, y2)].
'''
def error(T, Q, e):
    c = np.linalg.solve(Q, np.zeros(4))

    error = compute_E_H(T, c)

    return error

'''
vertex_link(T, v) returns the link of vertex v = (x, y) in the triangulation T.
'''
def vertex_link(T, v):
    link = []

    for t in T:
        if v in t:
            other_vertices = [x for x in t if x != v]

            link.append(other_vertices[0])
            link.append(other_vertices[1])
            link.append((other_vertices[0], other_vertices[1]))

    return link

'''
edge_link(T, e) returns the link of edge e = [(x1, y1), (x2, y2)] in the triangulation T.
'''
def edge_link(T, e):
    link = []

    for t in T:
        if e[0] in t and e[1] in t:
            for v in t:
                if v != e[0] and v != e[1]:
                    link.append(v)
                    break

    return link

'''
is_safe(T, e) returns True if it is safe to contract edge e = [(x1, y1), (x2, y2)] in the 
triangulation T using the link condition lemma.
'''
def is_safe(T, e):
    link_ab = edge_link(T, e)
    link_a = vertex_link(T, e[0])
    link_b = vertex_link(T, e[1])

    return set(link_ab) == set(link_a).intersection(set(link_b))

'''
contract_edge(T, e) contracts edge e = [(x1, y1), (x2, y2)] in the triangulation T.
'''
def contract_edge(T, e):
    middle_point = [(e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2]

    to_remove = []

    for i in range(0, len(T)):
        if e[0] in T[i] and e[1] in T[i]:
            to_remove.append(i)
        elif e[0] in T[i]:
            T[i].remove(e[0])
            T[i].append(middle_point)
        elif e[1] in T[i]:
            T[i].remove(e[1])
            T[i].append(middle_point)

    for i in range(0, len(to_remove)):
        T.pop(to_remove[i] - i)

def main():
   
    # T = [[(0, 0), (1, 0), (1, 1)], [(1, 0), (2, 0), (2, 1)], [(2, 0), (3, 0), (3, 1)], [(0, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1)], [(2, 0), (2, 1), (3, 1)]]

    T = [[(0, 2), (2, 2), (1, 4)], [(0, 2), (2, 2), (1, 0)], [(0, 2), (1, 4), (0, 4)], [(2, 2), (1, 4), (2, 4)], [(0,2), (1,0), (0,0)], [(2,2),(2,0),(1,0)]]
    
    T = [[(x, y, 0) for (x, y) in inner_list] for inner_list in T]
    print(T)

    edges = []
    for t in T:
        if (t[0], t[1]) not in edges:
            edges.append(sorted((t[0], t[1])))
        if (t[1], t[2]) not in edges:
            edges.append(sorted((t[1], t[2])))
        if (t[2], t[0]) not in edges:
            edges.append(sorted((t[2], t[0])))

    Q = compute_Q(T)

    print(Q)

    edges.sort(key=lambda e: error(T, Q, e))

    # for t in T:
    #     plt.plot([t[0][0], t[1][0]], [t[0][1], t[1][1]], 'k--')
    #     plt.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]], 'k--')
    #     plt.plot([t[2][0], t[0][0]], [t[2][1], t[0][1]], 'k--')

    # print(is_safe(T, [(0, 2), (2, 2)]))

    # contract_edge(T, [(0, 2), (2, 2)])

    # for t in T:
    #     plt.plot([t[0][0], t[1][0]], [t[0][1], t[1][1]], 'r')
    #     plt.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]], 'r')
    #     plt.plot([t[2][0], t[0][0]], [t[2][1], t[0][1]], 'r')

    # plt.show()

if __name__ == '__main__':
    main()