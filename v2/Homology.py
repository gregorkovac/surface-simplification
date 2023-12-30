from Simplify import Simplify
# from dionysus import Simplex, Filtration, data_cmp, data_dim_cmp, DynamicPersistenceChains
import dionysus as d

def main():
    file_path = "../output/bun_full_res/bun_5000.obj"

    simplify = Simplify(file_path)

    simplices = simplify.hasse.get_all_simplices()

    # Compute persistent homology
    f = d.Filtration(simplices)
    m = d.homology_persistence(f)
    dgms = d.init_diagrams(m, f)

    # Print homology information
    for i, dgm in enumerate(dgms):
        num_generators = len(dgm)
        print(f"H_{i}: {num_generators}")
        # for j, pt in enumerate(dgm):
        #     birth, death = pt
        #     print(f"Generator {j + 1}: Birth = {birth}, Death = {death}")

if __name__ == "__main__":
    main()