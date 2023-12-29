from Simplify import Simplify
from matplotlib import pyplot as plt
import random
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

random.seed(0)
np.random.seed(0)

def main():
    # path = "../models/ico_sphere.obj"
    path = "../models/bun_zipper_res4.ply"
    # path = "../models/bun_zipper_res4.obj"
    simplify = Simplify(path)
    #simplify.heap.print_heap()
    T = simplify.simplify(n = 0)

    TRI = simplify.abs2geo(T)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # draw edges of triangles
    for t in TRI:
        # ax.plot([t[0][0], t[1][0]], [t[0][1], t[1][1]], [t[0][2], t[1][2]], 'k')
        # ax.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]], [t[1][2], t[2][2]], 'k')
        # ax.plot([t[2][0], t[0][0]], [t[2][1], t[0][1]], [t[2][2], t[0][2]], 'k')

        triangle = Poly3DCollection([t], facecolors='lightgrey', edgecolors='k')
        # triangle.set_color('lightgrey')
        ax.add_collection3d(triangle)
    
    ax.grid(False)
    ax.set_axis_off()

    ax.set_xlim(-0.1, 0.1)
    ax.set_ylim(-0.1, 0.1)
    ax.set_zlim(-0.1, 0.1)
    plt.show()

if __name__ == "__main__":
    main()