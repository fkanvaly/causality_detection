import pandas as pd
from ocik.network import BayesianNetwork
from ocik.example import asia


def update_evidence(bnet: BayesianNetwork, data: pd.DataFrame):
    """
    update the parameter with respect to on data row
    :param bnet: bayesian network
    :param data: dataframe with one row data
    """
    network = bnet.get_network(data=True)

    for node, node_data in dict(network).items():
        parent, cpd = node_data.values()
        name = {1: bnet.name(node, 1),
                0: bnet.name(node, 0)}

        # node without parents
        if len(parent) == 0:
            count = data[node].value_counts()
            for i in list(count.index):
                cpd[name[i]] += count[i]
            continue

        # nbtime( node=a | par(node)=u)
        gpr = [*parent, node]
        df_count = data[gpr].reset_index().groupby(gpr).count()

        for index in list(df_count.index):
            by, i = index[:-1], index[-1]
            cpd.loc[by][name[i]] += df_count.loc[index][0]



