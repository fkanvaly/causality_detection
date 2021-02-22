from ocik.example import Asia, Room
from ocik.structure.doPC import doPC
from graphviz import Digraph, Graph, Source


def draw(edge, directed=True):
    dot = Digraph() if directed else Graph()
    dot.edges(edge)
    return dot


asia = Asia()
df = asia.load_data(1000)

orientation = set()
estimator = doPC(data=df)
model = estimator.estimate(variant='stable', max_cond_vars=4,
                           ci_test="do_ci",
                           do_node=df.columns,
                           env=asia.bn,
                           orientation=orientation,
                           )

print("orientation:", orientation)
