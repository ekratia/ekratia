from ekratia.delegates.models import Delegate
import networkx as nx
import logging
import random
logger = logging.getLogger('ekratia')


class GraphEkratia(nx.DiGraph):

    def __init__(self, *args, **kwargs):
        super(GraphEkratia, self).__init__(*args, **kwargs)
        self.visited = set()
        self.queue = []
        self.exclude = []

    def add_users_ids(self, users_ids):
        for user_id in users_ids:
            self.add_user_id(user_id)

    def add_user_id(self, user_id):
        logger.debug("Add User %i" % user_id)
        self.queue_node(user_id)
        while self.queue:
            current = self.retrieve_node()
            if current not in self.visited and current not in self.exclude:
                self.add_node(current)
                self.attach_predecessors(current)
                self.attach_succesors(current)
                self.visit_node(current)

    def set_exclude_list(self, users_ids):
        self.exclude = users_ids

    def visit_node(self, node):
        logger.debug("Visited %i" % node)
        self.visited.add(node)

    def queue_node(self, node):
        logger.debug("Queued %i" % node)
        self.queue.append(node)

    def retrieve_node(self):
        return self.queue.pop(0)

    def attach_predecessors(self, node):
        logger.debug("attach_predecessors")
        predecessors = self.get_user_id_delegates_to_me(node)
        for predecessor in predecessors:
            if predecessor not in self.exclude:
                self.add_node(predecessor)
                self.add_edge(predecessor, node)
                self.queue_node(predecessor)

    def attach_succesors(self, node):
        logger.debug("attach_succesors")
        successors = self.get_user_id_delegates(node)
        for successor in successors:
            if successor not in self.exclude:
                self.add_node(successor)
                self.add_edge(node, successor)
                self.queue_node(successor)

    def get_user_id_delegates(self, user_id):
        return Delegate.objects.filter(user__id=user_id)\
            .values_list('delegate__id', flat=True)

    def get_user_id_delegates_to_me(self, user_id):
        return Delegate.objects.filter(delegate__id=user_id)\
            .values_list('user__id', flat=True)

    def get_pagerank_values(self):
        return nx.pagerank_numpy(self)

    def set_nodes_pagerank(self):
        values = nx.pagerank_numpy(self)
        for key in values.keys():
            self.node[key]['pagerank'] = values[key]
        return values

    def set_nodes_pagerank_normalized(self):
        count = self.number_of_nodes()
        pageranks = self.set_nodes_pagerank()
        for key in pageranks.keys():
            self.node[key]['pagerank_normalized'] = pageranks[key] * count

    def set_vote_value(self, user_id):
        values = self.get_pagerank_values()
        # self.node[user_id]['rank'] = values[user_id] * self.number_of_nodes()

        for key in values.keys():
            if 'rank' not in self.node[key]:
                self.node[key]['rank'] = values[key] * self.number_of_nodes()

    def get_node_users(self):
        from ekratia.users.models import User
        users = User.objects.filter(id__in=self.nodes())
        return users

    def set_users_properties(self):
        for user in self.get_node_users():
            self.node[user.id]['name'] = user.get_full_name_or_username
            self.node[user.id]['avatar'] = user.get_avatar

    def get_sigma_representation(self):
        self.set_users_properties()

        nodes = []
        edges = []
        for node in self.in_degree().keys():
            # TODO: Very nasty
            rank = self.node[node]['rank'] if 'rank' in self.node[node] else 0
            color = "green" if 'voted' in self.node[node] else "#ccc"
            node_dict = {
                          "id": str(node),
                          "label": "%s(%0.2f)" % (self.node[node]['name'],
                                                  rank),
                          "type": "image",
                          "url": self.node[node]['avatar'],
                          "x": random.random(),
                          "y": random.random(),
                          "size": 16,
                          "color": color
                        }
            nodes.append(node_dict)

        for edge in self.edges():
            edge_dict = {
                          "id": "e%i-%i" % edge,
                          "source": str(edge[0]),
                          "target": str(edge[1]),
                          "type": "curvedArrow",
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
