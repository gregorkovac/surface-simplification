from Simplify import Simplify
from matplotlib import pyplot as plt
import random
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time

# random.seed(0)
# np.random.seed(0)

NUM_CONTRACTIONS = 20000

def main():
    start = time.time()

    # path = "../models/ico_sphere.obj"
    # path = "../models/cube.obj"
    # path = "../models/bun_zipper.ply"
    path = "../output/bun_v3/bun_20000.obj"
    # path = "../models/bun_zipper_res4.obj"
    simplify = Simplify(path)
    #simplify.heap.print_heap()
    T = simplify.simplify(n = NUM_CONTRACTIONS, error_threshold=10)
    # print(len(T))

    elapsed = time.time() - start

    print("Finished in {} seconds".format(elapsed))

    simplify.export_obj(T, "../output/bun_v3/bun_{}.obj".format(2*NUM_CONTRACTIONS))

#     TRI = simplify.abs2geo(T)
    
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     # draw edges of triangles
#     for t in TRI:
#         triangle = Poly3DCollection([t], facecolors='lightgrey', edgecolors='k')
#         # triangle.set_color('lightgrey')
#         ax.add_collection3d(triangle)

#     ax.grid(False)
#     ax.set_axis_off()
#     ax.set_box_aspect((2, 2, 2))
# #
#     ax.set_xlim(-0.1, 0.1)
#     ax.set_ylim(-0.1, 0.1)
#     ax.set_zlim(-0.1, 0.1)
#     plt.show()

if __name__ == "__main__":
    main()