from django.test import TestCase
from .graphs import get_graph_value

import networkx as nx


class GraphTestCase(TestCase):
    def setUp(self):
        G = nx.DiGraph()
        G.add_node(1)
        G.add_node(2)
        G.add_node(3)
        G.add_node(4)
        self.G = G

    def test_graph_level0(self):
        G = self.G
        G.add_edge(2, 1)
        G.add_edge(3, 1)
        G.add_edge(4, 1)
        self.assertEqual(get_graph_value(G, 1), 4.0)
        self.assertEqual(get_graph_value(G, 2), 1)
        self.assertEqual(get_graph_value(G, 3), 1)
        self.assertEqual(get_graph_value(G, 4), 1)

    def test_graph_level1(self):
        G = self.G
        G.add_edge(3, 1)
        G.add_edge(4, 1)
        G.add_edge(4, 2)
        self.assertEqual(get_graph_value(G, 1), 2.5)
        self.assertEqual(get_graph_value(G, 2), 1.5)
        self.assertEqual(get_graph_value(G, 3), 1)
        self.assertEqual(get_graph_value(G, 4), 1)

    def test_graph_level2(self):
        G = self.G
        G.add_edge(3, 1)
        G.add_edge(4, 1)
        G.add_edge(4, 2)
        self.assertEqual(get_graph_value(G, 1), 2.5)
        self.assertEqual(get_graph_value(G, 2), 1.5)
        self.assertEqual(get_graph_value(G, 3), 1)
        self.assertEqual(get_graph_value(G, 4), 1)
