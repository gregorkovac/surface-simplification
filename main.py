from Simplify import Simplify
from matplotlib import pyplot as plt
import random
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time

random.seed(0)
np.random.seed(0)

NUM_CONTRACTIONS = 450

def main():
    start = time.time()

    path = "../models/sphere.obj"
    simplify = Simplify(path)
    T = simplify.simplify(n = NUM_CONTRACTIONS, error_threshold=10)

    elapsed = time.time() - start

    print("Finished in {} seconds".format(elapsed))

    simplify.export_obj(T, "../output/sphere/sphere_{}.obj".format(NUM_CONTRACTIONS))

if __name__ == "__main__":
    main()