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

