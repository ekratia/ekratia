import networkx as nx
from ekratia.core import graphs
# Example 1
G = nx.DiGraph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_edge(2, 1)
# G.add_edge(3, 1)
G.add_edge(4, 2)
G.add_edge(4, 3)
# Circular:
G.add_edge(1, 4)
graphs.count_total_predecessors(G, 1)

# Example 2

G = nx.DiGraph()
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_edge(2, 1)
G.add_edge(3, 2)
G.add_edge(4, 3)
G.add_edge(1, 4)
G.add_edge(2, 3)
