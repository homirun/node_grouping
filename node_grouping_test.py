from node_grouping.node_network import *
from node_grouping.node_list import *
import uuid
import threading
import time
import logging


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def main():
    print('/*----main----*/')
    node_list = _init_connect_network()
    api_server_thread = threading.Thread(target=start_api_server, name='api_server')
    # api_server_thread.setDaemon(True)
    api_server_thread.start()


def _init_connect_network():
    print('/*----init_connect_network----*/')
    node_list = NodeList()
    my_ip = ifaddresses('en0')[AF_INET][0]['addr']
    request_ip = input('request_ip:')
    res = throw_add_request(node_list, request_ip, my_ip)
    if res is False:
        # もし他のノードが存在しなかった時
        node_list.add_my_node()
    else:
        # resの値をnode_listへ
        pass
    return node_list


if __name__ == '__main__':
    main()
