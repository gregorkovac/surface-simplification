import matplotlib.pyplot as plt

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

def main():
   
    T = [[(0, 0), (1, 0), (1, 1)], [(1, 0), (2, 0), (2, 1)], [(2, 0), (3, 0), (3, 1)], [(0, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1)], [(2, 0), (2, 1), (3, 1)]]


    for t in T:
        plt.plot([t[0][0], t[1][0]], [t[0][1], t[1][1]], 'k--')
        plt.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]], 'k--')
        plt.plot([t[2][0], t[0][0]], [t[2][1], t[0][1]], 'k--')

    contract_edge(T, [(0, 0), (1, 1)])

    for t in T:
        plt.plot([t[0][0], t[1][0]], [t[0][1], t[1][1]], 'r')
        plt.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]], 'r')
        plt.plot([t[2][0], t[0][0]], [t[2][1], t[0][1]], 'r')

    plt.show()

if __name__ == '__main__':
    main()