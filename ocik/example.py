from ocik.network import BayesianNetwork
import pandas as pd


class Asia:
    __data = "ocik/demo/store/asia.csv"

    def __init__(self):
        ed = lambda a, b: [f'{a}', f'{b}']

        self.bn = BayesianNetwork([ed("A", "T"), ed("T", "O"),
                                   ed("S", "L"), ed("L", "O"),
                                   ed("S", "B"), ed("B", "D"),
                                   ed("O", "X"), ed("O", "D")])

        self.bn.set_cpd("A", [[0.99], [0.01]], [])
        self.bn.set_cpd("T", [[0.99, 0.95],
                              [0.01, 0.05]], ["A"])
        self.bn.set_cpd("S", [[0.5], [0.5]], [])
        self.bn.set_cpd("L", [[0.99, 0.90],
                              [0.01, 0.10]], ["S"])
        self.bn.set_cpd("B", [[0.7, 0.4],
                              [0.3, 0.6]], ["S"])
        self.bn.set_cpd("X", [[0.95, 0.02],
                              [0.05, 0.98]], ["O"])
        self.bn.set_cpd("O", [[0.1, 0.0, 0.0, 0.0],
                              [0.9, 1.0, 1.0, 1.0]], ["T", "L"])
        self.bn.set_cpd("D", [[0.9, 0.2, 0.3, 0.1],
                              [0.1, 0.8, 0.7, 0.9]], ["O", "B"])

    def get_network(self):
        return self.bn

    def load_data(self, nrows=100):
        return pd.read_csv(self.__data, nrows=nrows)


class Room:
    __data = "ocik/demo/store/room.csv"

    def __init__(self):
        ed = lambda a, b: [f'{a}', f'{b}']

        bn = BayesianNetwork([ed("P", "H"), ed("P", "L"),
                              ed("H", "T"), ed("W", "T")])

        bn.set_cpd("P", [[0.6], [0.4]], [])
        bn.set_cpd("W", [[0.3], [0.7]], [])

        bn.set_cpd("H", [[0.1, 0.5],
                         [0.9, 0.5]], ["P"])

        bn.set_cpd("L", [[0.2, 0.9],
                         [0.8, 0.1]], ["P"])

        bn.set_cpd("T", [[0.05, 0.3, 0.4, 0.9],
                         [0.95, 0.7, 0.6, 0.1]], ["H", "W"])

        self.bn = bn

    def get_network(self):
        return self.bn

    def load_data(self, nrows=100):
        return pd.read_csv(self.__data, nrows=nrows)


class Circuit:
    def __init__(self):
        fn = lambda k, v: f"{k}={v}"
        ed = lambda a, b: [f'x{a}', f'x{b}']

        bn = BayesianNetwork([ed(1, 4), ed(4, 8), ed(8, 9), ed(9, 11),
                              ed(2, 5), ed(2, 6), ed(6, 8), ed(6, 10), ed(10, 11),
                              ed(3, 5), ed(5, 6), ed(5, 7), ed(7, 10)])

        from ocik.porte import f_and, f_nand, f_nor, f_not, f_or, f_xor

        def fill(x, gate):
            val = int(x.name.split("=")[1])
            if len(x.index) == 1:
                return [gate(x)[val]]
            if type(x.index[0]) == tuple:
                return [int(gate(*idx) == val) for idx in x.index]
            else:
                return [int(gate(idx) == val) for idx in x.index]

        rand = lambda x: lambda u: [x, 1 - x]

        circuit = [('x1', rand(0.5)), ('x2', rand(0.5)), ('x3', rand(0.5)), ('x4', f_not), ('x5', f_nand),
                   ('x6', f_and), ('x7', f_not), ('x8', f_xor), ('x9', f_not), ('x10', f_xor), ('x11', f_xor)]

        for node, foo in circuit:
            cpd = bn.get_cpd(node)[1].apply(lambda x: fill(x, foo))
            bn._set_cpd(node, cpd)

        self.bn = bn