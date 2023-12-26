import numpy as np

from tools import vertex_link, edge_link

'''
compute_Q(T) returns the fundamental quadratic matrix of the function E_H(x) used for error calculation.
'''
def compute_Q(T):
    # TODO: Check if this is correct
    Q = np.zeros((4, 4))

    for t in T:
        a, b, c = np.array(t[0]), np.array(t[1]), np.array(t[2])

        # v1 = np.array(b) - np.array(a)
        # v2 = np.array(x) - np.array(a)

        normal = np.cross(b - a, c - a)
        normal = normal / np.linalg.norm(normal)

        offset = -np.dot(normal, np.array(a))

        u = np.array([normal[0], normal[1], normal[2], offset])

        Q += np.outer(u, u)

    return Q

'''
compute_E_H(x) returns of the value of the E_H(x) function at point x using the fundamental quadratic matrix Q.
'''
def compute_E_H(x, Q):
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
error(T, e) returns the damage caused to the triangulation T by contracting an edge using its quadric.
'''
def error(T, Q):

    print(Q)

    c = np.linalg.solve(Q, np.zeros(4))

    error = compute_E_H(T, c)

    return error

'''
is_safe(T, e) returns True if it is safe to contract edge e in the 
triangulation T using the link condition lemma.
'''
def is_safe(T, e):
    link_ab = edge_link(T, e)
    link_a = vertex_link(T, e[0])
    link_b = vertex_link(T, e[1])

    return set(link_ab) == set(link_a).intersection(set(link_b))

'''
contract_edge(T, e) contracts edge e in the triangulation T.
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