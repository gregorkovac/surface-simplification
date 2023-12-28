from Simplify import Simplify
from matplotlib import pyplot as plt
import random
import numpy as np

random.seed(0)
np.random.seed(0)

def main():
    path = "models/cube.obj"
    simplify = Simplify(path)
    #simplify.heap.print_heap()
    T = simplify.simplify()

    TRI = simplify.abs2geo(T)


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # draw edges of triangles
    for t in TRI:
        ax.plot([t[0][0], t[1][0]], [t[0][1], t[1][1]], [t[0][2], t[1][2]], 'k')
        ax.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]], [t[1][2], t[2][2]], 'k')
        ax.plot([t[2][0], t[0][0]], [t[2][1], t[0][1]], [t[2][2], t[0][2]], 'k')
    plt.show()

if __name__ == "__main__":
    main()