import networkx as nx
import logging
logger = logging.getLogger('ekratia')


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
    count = 0
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
