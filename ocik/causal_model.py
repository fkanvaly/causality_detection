from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

def beta_dist(a, b):
    assert a + b > 2
    x = np.linspace(beta.ppf(0.001, a, b),
                    beta.ppf(0.999, a, b), 1000)
    y = beta.pdf(x, a, b)
    mod = (a - 1) / (a + b - 2)
    return x, y, mod


def plot_beta(a, b, ax=None, color="b", label=""):
    if ax is None:
        fig, ax = plt.subplots(1, 1)

    x, y, _ = beta_dist(a, b)
    ax.plot(x, y,
            lw=2, alpha=0.6, label=label, color=color)

    r = beta.rvs(a, b, size=1000)
    ax.hist(r, density=True, histtype='stepfilled', alpha=0.2, bins=20, color=color)
    ax.set_xlim(0, 1)


def simulate(query_node: str, watch_nodes: list, env, do_size=100, same_seed=True):
    result = {}
    evidences = [{query_node: value} for value in [0, 1]]

    for i, evidence in enumerate(evidences):
        seed = 0 if same_seed else i
        do_result = env.do(evidence=evidence, size=do_size, seed=seed)

        ev = evidence[query_node]
        result[ev] = {}
        for node in watch_nodes:
            counts = do_result[node].value_counts()
            a = counts[0] + 1 if 0 in counts.index else 1
            b = counts[1] + 1 if 1 in counts.index else 1  # for a beta dist we need to add 1
            _, _, mod = beta_dist(a, b)
            result[ev][node] = mod

    return result


def do_orientation(un_edges, env, verbose=False):
    G = nx.Graph(un_edges)
    orientation = []

    while len(G.edges()):
        ordered_degree = sorted(G.degree(), key=lambda item: -item[1])

        src = ordered_degree.pop()[0]
        neighb = list(G.neighbors(src))

        src_effect = simulate(src, neighb, env)
        dst_effect = {node: simulate(node, [src], env) for node in neighb}

        new_edges = []
        for dst in neighb:
            src_on_dst = abs(src_effect[0][dst] - src_effect[1][dst])
            dst_on_src = abs(dst_effect[dst][0][src] - dst_effect[dst][1][src])

            if src_on_dst > dst_on_src:
                new_edges.append((src, dst))
            else:
                new_edges.append((dst, src))

        G.remove_edges_from(new_edges)
        G.remove_node(src)
        orientation += new_edges

    return orientation
