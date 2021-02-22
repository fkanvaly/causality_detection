from BayesianNetwork import BayesianNetwork
from ocik.porte import f_and, f_nand, f_not, f_xor
import pandas as pd
import networkx as nx
from random import choice
from collections import defaultdict


def mask(df, key, value):
    return df[df[key] == value]


pd.DataFrame.mask = mask


def bn_example1():
    fn = lambda k, v: f"{k}={v}"
    ed = lambda a, b: [f'x{a}', f'x{b}']

    bn = BayesianNetwork([ed(1, 4), ed(4, 8), ed(8, 9), ed(9, 11),
                          ed(2, 5), ed(2, 6), ed(6, 8), ed(6, 10), ed(10, 11),
                          ed(3, 5), ed(5, 6), ed(5, 7), ed(7, 10)])

    def remplir(node, cpd, par, func):
        node_1 = fn(node, 1)
        node_0 = fn(node, 0)
        if len(par) == 0:
            cpd[node_1] = [0.5]
            cpd[node_0] = [0.5]
            return
        cpd[node_1] = cpd[par].apply(lambda x: int(func(*[x[p] for p in par]) == 1), axis=1)
        cpd[node_0] = cpd[par].apply(lambda x: int(func(*[x[p] for p in par]) == 0), axis=1)

        # on fait la meme chose pour tous les autres noeuds

    to_apply = {"x1": None, "x2": None, "x3": None, "x4": f_not, "x5": f_nand, "x6": f_and,
                "x7": f_not, "x8": f_and, "x9": f_not, "x10": f_xor, "x11": f_xor}

    for node, func in to_apply.items():
        par, cpd = bn.get_cpd(node)
        remplir(node, cpd, par, func)
        bn._set_cpd(node, cpd)

    return bn

def bn_example2():
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




def recover_independance(G: nx.Graph, df):
    G = G.copy()

    ind_test = IndependanceTest(df, correction=True)

    i = 0
    SepSet = {(Xa, Xb): set() for (Xa, Xb) in G.edges()}
    SepSet.update({(Xb, Xa): set([]) for (Xa, Xb) in G.edges()})

    adj = {(Xa, Xb): set(nx.neighbors(G, Xa)) - {Xb} for Xa in G.nodes()
           for Xb in set(G.nodes()) - {Xa}
           if G.has_edge(Xa, Xb)}

    to_remove = defaultdict(list)

    while max(list(map(len, adj.values()))) >= i:
        print('indépendance de niveau : ' + str(i))
        edges = list(G.edges()) + [e[::-1] for e in G.edges()]
        for edge in edges:
            Xa, Xb = edge
            if len(adj[(Xa, Xb)]) >= i:
                S = subset(list(adj[(Xa, Xb)]), i)
                is_delete = False
                for Xc in S:
                    if ind_test.khi2(Xa, Xb, Xc):
                        print(f"{Xa} _|_ {Xb} | {Xc}")
                        if not is_delete and (Xa, Xb) in G.edges():
                            G.remove_edge(Xa, Xb)
                            to_remove[i].append((Xa, Xb))
                            is_delete = True
                        SepSet[(Xa, Xb)] = SepSet[(Xa, Xb)] | set(Xc)
                        SepSet[(Xb, Xa)] = SepSet[(Xb, Xa)] | set(Xc)
        i += 1
        adj = {(Xa, Xb): set(nx.neighbors(G, Xa)) - {Xb} for Xa in G.nodes()
               for Xb in set(G.nodes()) - {Xa}
               if G.has_edge(Xa, Xb)}

    return SepSet, to_remove

def searchV(G: nx.Graph, df, SepSet):
    not_oriented = set(G.edges())

    # Recherche des V-structures
    DiG = nx.DiGraph()
    DiG.add_nodes_from(G.nodes())

    triplet = []
    # looking of Xa, Xb, Xc such that Xa-Xc-Xb with Xa and Xb not connected
    for Xc in G.nodes():
        common_neighb = list(G.neighbors(Xc))
        for (Xa, Xb) in subset(common_neighb, 2):
            if not G.has_edge(Xa, Xb) and Xc not in SepSet[(Xa, Xb)]:
                DiG_temp = DiG.copy()

                DiG_temp.add_edge(Xa, Xc)
                DiG_temp.add_edge(Xb, Xc)

                if nx.is_directed_acyclic_graph(DiG_temp):
                    DiG = DiG_temp
                    triplet.append((Xa,Xc,Xb))
                    not_oriented = not_oriented - {(Xa, Xc), (Xc, Xa), (Xb, Xc), (Xc, Xb)}
                    print(f"{Xa}->{Xc}<-{Xb}")

    return DiG, not_oriented, triplet

def ajout_recursif(DiG, G, not_oriented):
    oriented = []
    while len(not_oriented)>0:
        modif = 0
        nodes = set(G.nodes())
        DiG_inv = DiG.reverse()
        will_create_V = lambda e: len(list(DiG_inv.neighbors(e[1])))!=0

        def will_create_cycle(e) :
            DiiG = DiG.copy()
            DiiG.add_edge(e[0], e[1])
            return not nx.is_directed_acyclic_graph(DiiG)

        for Xa in nodes:
            for Xb in nodes - {Xa}:

                if isReachable(DiG, Xa, Xb) \
                        and G.has_edge(Xa, Xb)\
                        and (Xa, Xb) in not_oriented \
                        and not will_create_V((Xa, Xb)) \
                        and not will_create_cycle((Xa, Xb)):

                    DiG.add_edge(Xa, Xb)
                    oriented.append((Xa,Xb))
                    not_oriented = not_oriented - {(Xa, Xb), (Xb, Xa)}
                    modif = 1; print('orient')

                elif not G.has_edge(Xa, Xb):

                    neighb = DiG.neighbors(Xa)

                    for Xc in neighb:

                        if G.has_edge(Xc, Xb) \
                                and (Xc, Xb) in not_oriented \
                                and not will_create_V((Xc, Xb))\
                                and not will_create_cycle((Xc, Xb)):

                            DiG.add_edge(Xc, Xb)
                            oriented.append((Xc, Xb))
                            not_oriented = not_oriented - {(Xc, Xb), (Xb, Xc)}

                            modif=1;
                # else:
                #     cn = set(nx.common_neighbors(DiG, Xa, Xb)) & set(nx.neighbors(G, Xc))
                #     if len(cn)!=0:
                #         set(nx.neighbors(G, Xc)) for Xc in cn]
        if modif==0:
            edges = set([(e[1], e[0]) for e in not_oriented]) | not_oriented
            print(edges)
            no_V_edges = [e for e in edges if not will_create_V(e)
                          and not will_create_cycle(e)]
            if len(no_V_edges)==0:
                break
            e = choice(no_V_edges)
            not_oriented = not_oriented - {e, e[::-1]}
            DiG.add_edge(e[0], e[1])
            oriented.append(e)
            modif =1;

    return DiG, oriented


def PC(df: pd.DataFrame):
    # Construction d’un graphe non orienté
    ## graphe reliant complètement tous les noeuds
    edge_list = {node: [(node, u) for u in set(df.columns) - {node}] for node in df.columns}
    G = nx.Graph()
    for edges in edge_list.values():
        G.add_edges_from(edges)

    SepSet, edge_to_remove = recover_independance(G, df)
    for edges in edge_to_remove.values():
        G.remove_edges_from(edges)

    not_oriented = set(G.edges())

    # Recherche des V-structures
    DiG, not_oriented, _ = searchV(G, df, SepSet)

    # Ajout recurssif
    DiG, _ = ajout_recursif(DiG, G, not_oriented)
    return G, DiG

