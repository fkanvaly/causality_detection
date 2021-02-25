from ocik.example import Asia, Room, Circuit
from ocik.structure.doPC import doPC
from graphviz import Digraph, Graph, Source


def draw(edge, directed=True):
    dot = Digraph() if directed else Graph()
    dot.edges(edge)
    return dot


network = Asia()
bn = network.bn
df = bn.sample(2)

orientation = set()
estimator = doPC(data=df)
model = estimator.estimate(variant='stable', max_cond_vars=4,
                           ci_test="do_ci",
                           do_node=df.columns,
                           env=bn,
                           orientation=orientation,
                           )

print("orientation:", orientation)
