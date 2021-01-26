from ocik.network import BayesianNetwork


def asia():
    ed = lambda a, b: [f'{a}', f'{b}']

    bn = BayesianNetwork([ed("A", "T"), ed("T", "O"),
                          ed("S", "L"), ed("L", "O"),
                          ed("S", "B"), ed("B", "D"),
                          ed("O", "X"), ed("O", "D")])

    bn.set_cpd("A", [[0.99], [0.01]], [])
    bn.set_cpd("T", [[0.99, 0.95],
                     [0.01, 0.05]], ["A"])
    bn.set_cpd("S", [[0.5], [0.5]], [])
    bn.set_cpd("L", [[0.99, 0.90],
                     [0.01, 0.10]], ["S"])
    bn.set_cpd("B", [[0.7, 0.4],
                     [0.3, 0.6]], ["S"])
    bn.set_cpd("X", [[0.95, 0.02],
                     [0.05, 0.98]], ["O"])
    bn.set_cpd("O", [[0.1, 0.0, 0.0, 0.0],
                     [0.9, 1.0, 1.0, 1.0]], ["T", "L"])
    bn.set_cpd("D", [[0.9, 0.2, 0.3, 0.1],
                     [0.1, 0.8, 0.7, 0.9]], ["O", "B"])

    return bn