from node_grouping.node_network import *
from node_grouping.node_list import *


def main():
    node_list = _init_connect_network()


def _init_connect_network():
    node_list = NodeList()
    throw_add_request(node_list)
    return node_list


if __name__ == '__main__':
    main()
