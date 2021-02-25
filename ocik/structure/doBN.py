#!/usr/bin/env python

from warnings import warn
from itertools import combinations, permutations, chain

import networkx as nx
from tqdm import tqdm

from pgmpy.estimators import StructureEstimator
from pgmpy.global_vars import SHOW_PROGRESS

from ocik.independence import ci_do, has_influence


class doPC(StructureEstimator):
    def __init__(self, data=None, independencies=None, **kwargs):
        super(doPC, self).__init__(data=data, independencies=independencies, **kwargs)

    def estimate(
            self,
            variant="stable",
            ci_test="chi_square",
            max_cond_vars=5,
            return_type="dag",
            significance_level=0.01,
            n_jobs=-1,
            show_progress=True,
            **kwargs,
    ):
        # Step 1: Run the PC algorithm to build the skeleton and get the separating sets.
        skel, _ = self.build_skeleton(
            ci_test=ci_test,
            max_cond_vars=max_cond_vars,
            significance_level=significance_level,
            variant=variant,
            n_jobs=n_jobs,
            show_progress=show_progress,
            **kwargs,
        )
        return skel

    def build_skeleton(
            self,
            ci_test="chi_square",
            max_cond_vars=5,
            significance_level=0.01,
            variant="stable",
            n_jobs=-1,
            show_progress=True,
            **kwargs,
    ):
        # Initialize initial values and structures.
        ci_test = ci_do
        lim_neighbors = 0
        separating_sets = dict()

        if show_progress and SHOW_PROGRESS:
            pbar = tqdm(total=max_cond_vars)
            pbar.set_description("Working for n conditional variables: 0")

        # Step 1: Initialize a fully connected undirected graph
        completeG = nx.complete_graph(n=self.variables, create_using=nx.Graph)
        G = nx.DiGraph(list(completeG.edges()))
        graph = nx.DiGraph(list(G.edges()) + list(G.reverse().edges()))
        # Exit condition: 1. If all the nodes in graph has less than `lim_neighbors` neighbors.
        #             or  2. `lim_neighbors` is greater than `max_conditional_variables`.
        while not all(
                [len(list(graph.neighbors(var))) < lim_neighbors for var in self.variables]
        ):
            # Step 2: Iterate over the edges and find a conditioning set of
            # size `lim_neighbors` which makes u and v independent.
            # In case of stable, precompute neighbors as this is the stable algorithm.
            if lim_neighbors == 0:
                print("direct influence")
                influence = {}
                for node in graph.nodes():
                    influence[node] = has_influence(node, list(graph.neighbors(node)), [], kwargs['env'])

                print('start test')
                edges = list(graph.edges())
                for (X, Y) in edges:
                    print('test :', X, Y)
                    X2Y = influence[X][Y]
                    Y2X = influence[Y][X]
                    influences = any([X2Y, Y2X])
                    if 'orientation' in kwargs and influences:
                        if X2Y:
                            kwargs['orientation'].add((X, Y))
                        if Y2X:
                            kwargs['orientation'].add((Y, X))
                    elif not influences:
                        graph.remove_edge(X, Y)
                        print(X, Y, 'remove')
                        if (X, Y) in kwargs['orientation']:
                            kwargs['orientation'].remove((X, Y))
                        if (Y, X) in kwargs['orientation']:
                            kwargs['orientation'].remove((Y, X))

            elif lim_neighbors > 0:
                print("conditional influence")
                influence = {}
                for node in graph.nodes():
                    neigh = set(graph.neighbors(node))
                    all_sep_set = set()
                    for v in neigh:
                        all_sep_set = all_sep_set | set(combinations(set(graph.neighbors(node)) - {v}, lim_neighbors))

                    influence[node] = {}
                    for sep_set in list(all_sep_set):
                        on = neigh - set(sep_set)
                        if len(on) > 0:
                            influence[node][sep_set] = has_influence(node, list(on), sep_set, kwargs['env'])

                edges = list(graph.edges())
                for (X, Y) in edges:
                    for separating_set in list(
                            set(combinations(set(graph.neighbors(X)) - {Y}, lim_neighbors))
                    ):
                        # If a conditioning set exists remove the edge, store the
                        # separating set and move on to finding conditioning set for next edge.
                        the_sep_set = None
                        for sep_set in influence[X].keys():
                            if set(sep_set) == set(separating_set):
                                x_set = sep_set
                                break

                        assert the_sep_set is not None
                        if influence[]
                        if ci_test(
                                X,
                                Y,
                                separating_set,
                                data=self.data,
                                independencies=self.independencies,
                                significance_level=significance_level,
                                **kwargs,
                        ):
                            print(X, Y, '|', separating_set)
                            graph.remove_edge(X, Y)
                            break

            # Step 3: After iterating over all the edges, expand the search space by increasing the size
            #         of conditioning set by 1.
            if lim_neighbors >= max_cond_vars:
                warn("Reached maximum number of allowed conditional variables. Exiting")
                break
            lim_neighbors += 1

            if show_progress and SHOW_PROGRESS:
                pbar.update(1)
                pbar.set_description(
                    f"Working for n conditional variables: {lim_neighbors}"
                )
        if show_progress and SHOW_PROGRESS:
            pbar.close()
        return graph, separating_sets
