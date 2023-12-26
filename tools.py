'''
vertex_link(T, v) returns the link of vertex v in the triangulation T.
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
edge_link(T, e) returns the link of edge e in the triangulation T.
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
triangles_with_vertex(T, v) returns the triangles in the triangulation T that contain vertex v.
'''
def triangles_with_vertex(T, v):
    triangles = []

    for t in T:
        if v in t:
            triangles.append(t)

    return triangles

'''
triangles_with_edge(T, e) returns the triangles in the triangulation T that contain the edge e.
'''
def triangles_with_edge(T, e):
    triangles = []

    for t in T:
        if e[0] in t and e[1] in t:
            triangles.append(t)

    return triangles

'''
get_edges_and_vertices(T) returns the edges and vertices of the triangulation T.
'''
def get_edges_and_vertices(T):
    E = []
    V = []
    for t in T:
        if (t[0], t[1]) not in E:
            E.append(sorted((t[0], t[1])))
        if (t[1], t[2]) not in E:
            E.append(sorted((t[1], t[2])))
        if (t[2], t[0]) not in E:
            E.append(sorted((t[2], t[0])))

        if t[0] not in V:
            V.append(t[0])
        if t[1] not in V:
            V.append(t[1])
        if t[2] not in V:
            V.append(t[2])

    return E, V