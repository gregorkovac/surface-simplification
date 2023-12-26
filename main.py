import matplotlib.pyplot as plt
import numpy as np

from simplification import compute_Q, compute_E_H, error, is_safe, contract_edge
from tools import triangles_with_vertex, triangles_with_edge, get_edges_and_vertices, obj_to_triangulation

def main():

    T = obj_to_triangulation('models/ico_sphere.obj')
   
    # T = [[(0, 0), (1, 0), (1, 1)], [(1, 0), (2, 0), (2, 1)], [(2, 0), (3, 0), (3, 1)], [(0, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1)], [(2, 0), (2, 1), (3, 1)]]

    # T = [[(0, 2), (2, 2), (1, 4)], [(0, 2), (2, 2), (1, 0)], [(0, 2), (1, 4), (0, 4)], [(2, 2), (1, 4), (2, 4)], [(0,2), (1,0), (0,0)], [(2,2),(2,0),(1,0)]]
    
    # T = [[(x, y, 0) for (x, y) in inner_list] for inner_list in T]

    E, V = get_edges_and_vertices(T)

    # Store quadrics for all edges, vertices and triangles
    Q = {}
    for t in T:
        Q[tuple(sorted(t))] = compute_Q([t])
    
    for e in E:
        # TODO: What do we do with the edges that are contained in only one triangle?
        twe = triangles_with_edge(T, e)
        q = np.zeros((4, 4))
        for t in twe:
            q += Q[tuple(sorted(t))]
        Q[tuple(sorted(e))] = q

    for v in V:
        twv = triangles_with_vertex(T, v)
        q = np.zeros((4, 4))
        for t in twv:
            q += Q[tuple(sorted(t))]
        Q[v] = q

    E.sort(key=lambda e: error(Q[tuple(sorted(e))], e))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, e in enumerate(E):
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], [e[0][2], e[1][2]], 'k--')
        err = error(Q[tuple(sorted(e))], e)
        err = '{:.2e}'.format(err)
        
        ax.text((e[0][0] + e[1][0]) / 2, (e[0][1] + e[1][1]) / 2, (e[0][2] + e[1][2]) / 2, str(err))

    plt.show()

    # print(E)

    # Q = compute_Q(T)

    # E.sort(key=lambda e: error(T, Q, e))

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