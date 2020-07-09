from node_grouping.node_network import *
from node_grouping.node_list import *
from node_grouping.grouping import *
import os
import threading
import json
from multiprocessing import Value, Manager

import time
import logging


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
node_list = dict()
print('global')


def main():
    global node_list
    print('/*----main----*/')
    node_list = _init_connect_network()
    api_server_thread = threading.Thread(target=start_api_server, args=[node_list], name='api_server')
    # api_server_thread.setDaemon(True)
    api_server_thread.start()
    # TODO: sleep入れないとタイミングによっては変数の中がNONEになるのでエラーが出たら数秒後に再度ソートさせる処理を挟む
    time.sleep(5)
    print('node_list_main')
    print(node_list)
    grouping(node_list)


def _init_connect_network():
    print('/*----init_connect_network----*/')
    pre_node_list = None
    my_ip = None
    try:
        my_ip = ifaddresses('en0')[AF_INET][0]['addr']
    except ValueError:
        my_ip = ifaddresses('eth0')[AF_INET][0]['addr']
    finally:
        request_ip = input('request_ip:')
        res = throw_add_request(node_list, request_ip, my_ip)
        if res is False:
            # もし他のノードが存在しなかった時
            pre_node_list = create_node_list()
        else:
            # resの値をnode_listへ
            pre_node_list = res['node_list']

    return pre_node_list


if __name__ == '__main__':
    main()
