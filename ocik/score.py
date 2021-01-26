from tqdm import tqdm
import pandas as pd
import numpy as np


def likelihood_score(bn, data: pd.DataFrame):
    """
    return de likelihood score
    :param data:
    :return:
    """
    score = 0
    for i in tqdm(range(len(data))):
        df = data[i:i + 1]
        for node in bn.G.nodes():
            par, cpd = bn.get_cpd(node)
            selected = [node, *par]
            df_node = df[selected]  # select colomn concert by this node

            #  ########## TO change#################
            # we seach row corresponding to the parent value in the data
            cpd_row = cpd.copy()
            node_value = None
            for col in df_node:
                val = df_node[col][df_node.index[0]]
                if col == node:
                    node_value = val
                    continue  # we will treat this at the end
                cpd_row = cpd_row.mask(col, val)

            # we get the probability
            assert node_value is not None
            score += np.log(cpd_row[bn.name(node, node_value)][cpd_row.index[0]])

            ####################################

    return score
