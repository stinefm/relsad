from relsad.network.components import ICTLine, ICTNode


def is_connected(
    node_1: ICTNode,
    node_2: ICTNode,
    network,
):
    """
    Function that checks if node 1 and node 2 are connected using
    a depth first search

    Parameters
    ----------
    node_1 : ICTNode
        ICT node 1
    node_2 : ICTNode
        ICT node 2
    network : ICTNetwork
        ICT network

    Returns
    -------
    connected : bool
        Boolean variable stating whether the ICT nodes are connected

    """
    connected = False

    visited_nodes = {node: False for node in network.nodes}

    stack = [node_1]

    while len(stack) > 0:
        node = stack.pop()
        if node == node_2:
            connected = True
        if visited_nodes[node] is False:
            visited_nodes[node] = True
        for neighbor_node in node.get_neighbor_nodes():
            if visited_nodes[neighbor_node] is False:
                stack.append(neighbor_node)

    return connected
