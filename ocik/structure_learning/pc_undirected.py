from ocik.structure_learning._utils import IndependanceTest, subset
import networkx as nx
from collections import defaultdict
import pandas as pd


def recover_independance(G: nx.Graph, df, verbose=False):
    G = G.copy()

    ind_test = IndependanceTest(df, correction=True)

    i = 0
    adj = {(Xa, Xb): set(nx.neighbors(G, Xa)) - {Xb} for Xa in G.nodes()
           for Xb in set(G.nodes()) - {Xa}
           if G.has_edge(Xa, Xb)}

    to_remove = defaultdict(list)

    while max(list(map(len, adj.values()))) >= i:
        print('indépendance de niveau ' + str(i))
        edges = list(G.edges()) + [e[::-1] for e in G.edges()]
        for edge in edges:
            Xa, Xb = edge
            if len(adj[(Xa, Xb)]) >= i:
                S = subset(list(adj[(Xa, Xb)]), i)
                is_delete = False
                for Xc in S:
                    if ind_test.khi2(Xa, Xb, Xc):
                        print(f"{Xa} ⟂ {Xb} | {Xc}") if verbose else None
                        if not is_delete and (Xa, Xb) in G.edges():
                            G.remove_edge(Xa, Xb)
                            to_remove[i].append((Xa, Xb))
                            is_delete = True
        i += 1
        adj = {(Xa, Xb): set(nx.neighbors(G, Xa)) - {Xb} for Xa in G.nodes()
               for Xb in set(G.nodes()) - {Xa}
               if G.has_edge(Xa, Xb)}

    return to_remove


def pc_undirected(df: pd.DataFrame, verbose=False):
    # Construction d’un graphe non orienté
    ## graphe reliant complètement tous les noeuds
    edge_list = {node: [(node, u) for u in set(df.columns) - {node}] for node in df.columns}
    G = nx.Graph()
    for edges in edge_list.values():
        G.add_edges_from(edges)

    edge_to_remove = recover_independance(G, df, verbose=verbose)
    for edges in edge_to_remove.values():
        G.remove_edges_from(edges)

    return G

