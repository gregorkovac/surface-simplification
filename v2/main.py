from Simplify import Simplify
from matplotlib import pyplot as plt
import random
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

random.seed(0)
np.random.seed(0)

def main():
    #path = "../models/ico_sphere.obj"
    path = "../models/cube.obj"
    #path = "../models/bun_zipper_res4.ply"
    # path = "../models/bun_zipper_res4.obj"
    simplify = Simplify(path)
    #simplify.heap.print_heap()
    T = simplify.simplify(n = -1, error_threshold=10)
    print(len(T))

    TRI = simplify.abs2geo(T)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # draw edges of triangles
    for t in TRI:
        triangle = Poly3DCollection([t], facecolors='lightgrey', edgecolors='k')
        # triangle.set_color('lightgrey')
        ax.add_collection3d(triangle)
    
    ax.grid(False)
    ax.set_axis_off()
    ax.set_box_aspect((2, 2, 2))
#
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    plt.show()

if __name__ == "__main__":
    main()