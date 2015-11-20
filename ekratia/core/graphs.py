from ekratia.delegates.models import Delegate
import networkx as nx
import logging
logger = logging.getLogger('ekratia')


class GraphEkratia(nx.DiGraph):

    def __init__(self, *args, **kwargs):
        super(GraphEkratia, self).__init__(*args, **kwargs)
        self.visited = set()
        self.queue = []

    def add_users_ids(self, users_ids):
        for user_id in users_ids:
            self.add_user_id(user_id)

    def add_user_id(self, user_id):
        logger.debug("Add User %i" % user_id)
        self.queue_node(user_id)
        while self.queue:
            logger.debug("while on %s" % self.queue)
            current = self.retrieve_node()
            if current not in self.visited:
                self.add_node(current)
                self.attach_predecessors(current)
                self.attach_succesors(current)
                self.visit_node(current)

    def visit_node(self, node):
        logger.debug("Visited %i" % node)
        self.visited.add(node)
        logger.debug("New Visited %s" % self.visited)

    def queue_node(self, node):
        logger.debug("Queued %i" % node)
        self.queue.append(node)
        logger.debug("New Queue %s" % self.queue)

    def retrieve_node(self):
        return self.queue.pop(0)

    def attach_predecessors(self, node):
        logger.debug("attach_predecessors")
        predecessors = self.get_user_id_delegates(node)
        for predecessor in predecessors:
            self.add_node(predecessor)
            self.add_edge(predecessor, node)
            self.queue_node(predecessor)

    def attach_succesors(self, node):
        logger.debug("attach_succesors")
        successors = self.get_user_id_delegates_to_me(node)
        for successor in successors:
            self.add_node(successor)
            self.add_edge(node, successor)
            self.queue_node(successor)

    def get_user_id_delegates(self, user_id):
        return Delegate.objects.filter(user__id=user_id)\
            .values_list('delegate__id', flat=True)

    def get_user_id_delegates_to_me(self, user_id):
        return Delegate.objects.filter(delegate__id=user_id)\
            .values_list('user__id', flat=True)

    def get_sigma_representation(self):
        nodes = []
        edges = []
        for node in self.nodes():
            node_dict = {
                          "id": str(node),
                          "label": "Node %i" % node,
                          "x": 0,
                          "y": 0,
                          "size": 3
                        }
            nodes.append(node_dict)

        for edge in self.edges():
            edge_dict = {
                          "id": "e%i-%i" % edge,
                          "source": edge[0],
                          "target": edge[1]
                        }

            edges.append(edge_dict)

        sigma_dict = {
            'nodes': nodes,
            'edges': edges
        }

        return sigma_dict


def compute_graph_total(G, node):
    nodes = G.nodes()
    if node not in nodes:
        raise ValueError

    logger.debug("Current: %s" % str(node))

    predecessors = G.predecessors(node)
    logger.debug("Predecessors: %s" % str(predecessors))
    successors = G.successors(node)

    num_succesors = len(successors) if len(successors) > 0 else 1.0
    num_predecessors = len(predecessors)

    logger.debug("successors: %s" % str(successors))

    value = 1.0

    for predecessor in predecessors:
        p_value, p_successors, p_predecessors =\
            compute_graph_total(G, predecessor)

        logger.debug("Prev successors: %s" % str(p_successors))
        logger.debug("Prev predecessors: %s" % str(p_predecessors))
        logger.debug("Prev value: %s" % str(p_value))

        value = value + p_value/p_successors
        logger.debug("SUM value: %s" % str(value))

    return value, num_succesors, num_predecessors


def get_graph_value(G, node):
    value, successors, predecessors =\
                compute_graph_total(G, node)
    return value


def graph_pagerank_values(G):
    values = nx.pagerank_numpy(G)
    graph_values = {i: values[i]*len(values) for i in values.keys()}
    return graph_values


def graph_pagerank_node_value(G, node):
    values = graph_pagerank_values(G)
    result = values.pop(node)
    result += sum([values[i] for i in values.keys()])
    return result


def count_total_predecessors(G, node, visited=None):
    if not visited:
        visited = []
    logger.debug("On: %s" % node)
    logger.debug("Visited: %s" % visited)
    count = 0.0
    visited.append(node)
    for subnode in predecessors_not_visited(G, node, visited):
        count += 1.0 + count_total_predecessors(G, subnode, visited)\
            / len(G.successors(subnode))
    return count


def predecessors_not_visited(G, node, visited):
    predecessors = []
    for subnode in G.predecessors(node):
        if subnode not in visited:
            predecessors.append(subnode)
    return predecessors
