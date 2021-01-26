import numpy as np
import pandas as pd


def _sample(bn, evidence: dict = None):
    if evidence is None:
        evidence = {}
    else:
        evidence = evidence.copy()

    node_available = set([]) | set(evidence.keys())
    to_compute = set(bn.G.nodes()) - set(evidence.keys())

    data = dict(bn.G.nodes(data=True))
    dependancies = {node: d for node, d in data.items()}

    for node in bn.node_sort:
        if node in to_compute:
            par, cpd = dependancies[node]['par'], dependancies[node]['cpd']

            # raise if topological sort fails
            assert node_available & set(par) == set(par), "parent evidence not available"

            node_1 = bn.name(node, 1)
            node_0 = bn.name(node, 0)
            if len(dependancies[node]['par']) == 0:
                prob_1, prob_0 = cpd[node_1][cpd.index[0]], cpd[node_0][cpd.index[0]]
            else:
                select = tuple(evidence[p][0] for p in par)
                prob = cpd.loc[select]
                prob_1, prob_0 = prob[node_1], prob[node_0]

            evidence[node] = [np.random.choice([1, 0], p=[prob_1, prob_0])]
            node_available = node_available | {node}
            to_compute = to_compute - {node}

    assert len(to_compute) == 0, "not every node have been sample"

    return pd.DataFrame(evidence)


def sample(bn, size=20):
    df = pd.DataFrame({node: [] for node in sorted(bn.G.nodes())}).astype(int)
    for i in range(size):
        df = pd.concat((df, _sample(bn)))
    df.reset_index(drop=True, inplace=True)
    return df
