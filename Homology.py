from Simplify import Simplify
import dionysus as d

def main():
    file_path = "../output/bun_34500.obj"

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

if __name__ == "__main__":
    main()