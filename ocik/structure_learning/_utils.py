import pandas as pd
import itertools
import numpy as np
import networkx as nx
from scipy.stats.distributions import chi2

class IndependanceTest:
    def __init__(self, df, correction=True):
        """
        :param df: dataframe
        :param correction: https://en.wikipedia.org/wiki/Yates%27s_correction_for_continuity
        """
        self.df = df
        self.correction = correction

    def filter(self, df_: pd.DataFrame, col_name, col_val):
        df = df_.copy()
        for col, val in zip(col_name, col_val):
            df = df.mask(col, val)
        return df

    def khi2_iter(self, dof, Xa: str, xa: int, Xb: str, xb: int, Xc: list = [], xc: list = []):
        Nc = len(self.filter(self.df, Xc, xc))  # nb_time(Xc) in df
        Nac = len(self.filter(self.df.mask(Xa, xa), Xc, xc))  # nb_time(Xa|Xc) in df
        Nbc = len(self.filter(self.df.mask(Xb, xb), Xc, xc))  # nb_time(Xb|Xc) in df

        # les occurrences théoriques
        if Nc==0:
            return 0

        Tabc = Nac * Nbc / Nc

        # les occurrences observées : le nombre d’occurrences de {XA = xa, XB = xb et XC = xc} ;
        Nabc = len(self.filter(self.df.mask(Xa, xa).mask(Xb, xb), Xc, xc))

        if Nabc == 0 and Tabc == 0:
            return 0

        return (np.abs(Nabc - Tabc) - 0.5) ** 2 / Tabc if self.correction and dof==1 else (Nabc - Tabc) ** 2 / Tabc

    def khi2(self, Xa, Xb, Xc: list = []):
        # varibales possibles values in string using bits
        nb_node = 2 + len(Xc)
        n = 2 ** nb_node  # number of combinations
        binaries = [f"%0{nb_node}d" % int(format(i, f'#0{n}b')[2:]) for i in range(n)]  # write in binary

        #chi2
        dof = 2 ** len(Xc)
        limit = chi2.ppf(0.95, df=dof)

        khi2_score = 0
        for binary in binaries:
            values = list(map(int, list(binary)))
            xa, xb, xc = values[0], values[1], values[2:]
            khi2_score += self.khi2_iter(dof, Xa, xa, Xb, xb, Xc, xc)

        return khi2_score < limit


def kbits(n, k):
    result = []
    for bits in itertools.combinations(range(n), k):
        s = ['0'] * n
        for bit in bits:
            s[bit] = '1'
        result.append(''.join(s))
    return result


def subset(seq, size):
    if size == 0:
        return [[]]
    l_permut = kbits(len(seq), size)
    l_permut = [list(map(int, list(idx))) for idx in l_permut]
    S = [np.array(seq)[np.where(np.array(idx) == 1)[0]].tolist() for idx in l_permut]
    return S
