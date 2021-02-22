from pgmpy.estimators.CITests import chi_square, pearsonr, independence_match
import pandas as pd

from scipy.stats import chisquare


def simulate(src: str, dst: list, env, cond_evidence: dict = {}, do_size=100, same_seed=True):
    result = {}
    evidences = [{src: value, **cond_evidence} for value in [0, 1]]

    for i, evidence in enumerate(evidences):
        seed = 0 if same_seed else i
        do_result = env.do_evidence(evidence=evidence, size=do_size, seed=seed)

        ev = evidence[src]
        result[ev] = {}
        for node in dst:
            counts = do_result[node].value_counts()
            a = counts[0] + 1 if 0 in counts.index else 1
            b = counts[1] + 1 if 1 in counts.index else 1  # for a beta dist we need to add 1
            # _, _, mod = beta_dist(a, b)
            result[ev][node] = [a, b]

    return result


def has_influence(src: str, dst: list, cond_node: list, env, do_size=100):
    n_node = len(cond_node)
    n = 2 ** n_node  # number of combinations
    binaries = [f"%0{n_node}d" % int(format(i, f'#0{n}b')[2:]) for i in range(n)]  # write in binary
    conditional_evidences = [{cond_node[i]: int(b[i]) for i in range(len(cond_node))} for b in binaries]
    test = {node: [] for node in dst}
    p_value_lim = 0.2
    for cond_evidence in conditional_evidences:
        res = simulate(src, dst, env, cond_evidence, do_size=do_size)
        for node in dst:
            test[node].append(chisquare(f_obs=res[0][node], f_exp=res[1][node])[1] <= p_value_lim)
    influence = {node: any(test[node]) for node in dst}
    # print(src, '|', cond_node ,'->', influence)
    return influence


def ci_do(X, Y, Z, data, boolean=True, **kwargs):
    X2Y = has_influence(X, [Y], Z, kwargs['env'])[Y] if not 'do_size' in kwargs \
        else has_influence(X, [Y], Z, kwargs['env'], kwargs['do_size'])[Y]

    Y2X = has_influence(Y, [X], Z, kwargs['env'])[X]if not 'do_size' in kwargs \
        else has_influence(Y, [X], Z, kwargs['env'], kwargs['do_size'])[X]

    influences = any([X2Y, Y2X])

    if 'orientation' in kwargs and influences:
        if X2Y:
            kwargs['orientation'].add((X, Y))
        if Y2X:
            kwargs['orientation'].add((Y, X))
    elif not influences:
        if (X, Y) in kwargs['orientation']:
            kwargs['orientation'].remove((X, Y))
        if (Y, X) in kwargs['orientation']:
            kwargs['orientation'].remove((Y, X))

    # print(X, Y, '|', Z)
    # print("keep" if influences else "remove")
    return not influences
