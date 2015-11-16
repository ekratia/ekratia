from django.test import TestCase
from ekratia.core import graphs

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
        self.assertEqual(graphs.get_graph_value(G, 1), 4.0)
        self.assertEqual(graphs.get_graph_value(G, 2), 1)
        self.assertEqual(graphs.get_graph_value(G, 3), 1)
        self.assertEqual(graphs.get_graph_value(G, 4), 1)

    def test_graph_level1(self):
        G = self.G
        G.add_edge(3, 1)
        G.add_edge(4, 1)
        G.add_edge(4, 2)
        self.assertEqual(graphs.get_graph_value(G, 1), 2.5)
        self.assertEqual(graphs.get_graph_value(G, 2), 1.5)
        self.assertEqual(graphs.get_graph_value(G, 3), 1)
        self.assertEqual(graphs.get_graph_value(G, 4), 1)

    def test_graph_level2(self):
        G = self.G
        G.add_edge(3, 1)
        G.add_edge(4, 1)
        G.add_edge(4, 2)
        self.assertEqual(graphs.get_graph_value(G, 1), 2.5)
        self.assertEqual(graphs.get_graph_value(G, 2), 1.5)
        self.assertEqual(graphs.get_graph_value(G, 3), 1)
        self.assertEqual(graphs.get_graph_value(G, 4), 1)


class GraphPagerankCase(TestCase):
    def setUp(self):
        G = nx.DiGraph()
        self.G = G

    def test_graph_0(self):
        G = self.G
        G.add_node(1)
        G.add_node(2)
        G.add_node(3)
        G.add_edge(2, 1)
        G.add_edge(3, 1)
        self.assertEqual(graphs.graph_pagerank_node_value(G, 1), 3.0)

    def test_graph_1(self):
        G = self.G
        G.add_node(1)
        G.add_node(2)
        G.add_node(3)
        G.add_node(4)
        G.add_node(5)
        G.add_edge(2, 1)
        G.add_edge(3, 1)
        G.add_edge(1, 4)
        G.add_edge(1, 5)
        print graphs.graph_pagerank_values(G)
        self.assertEqual(graphs.graph_pagerank_node_value(G, 4), 5.0)
        self.assertEqual(graphs.graph_pagerank_node_value(G, 5), 5.0)
