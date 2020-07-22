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
node_list = list()
secondary_node_list = list()
my_node_id = None


def main():
    global node_list, secondary_node_list, my_node_id
    print('/*----main----*/')
    my_node_id = create_node_id()
    node_list = _init_connect_network()
    api_server_thread = threading.Thread(target=start_api_server, args=[node_list], name='api_server')
    # api_server_thread.setDaemon(True)
    api_server_thread.start()

    # TODO:APIサーバがあがる前にgroupingを始めるとノード変更通知を送信できないノードが出てくるので暫定的処理
    time.sleep(3)
    # nodelistに更新があったらグルーピングを行う copyは値渡し
    grouping(node_list.copy())
    secondary_node_list = node_list.copy()
    while True:
        # time.sleep(3)
        # print('prime:')
        # print(node_list)
        # print('second:')
        # print(secondary_node_list)
        # print('id:')
        # print(id(node_list))
        sorted_node_list = boot_time_upper_sort(node_list)
        for i in range(len(sorted_node_list)):
            # print(i)
            if len(sorted_node_list) != len(secondary_node_list) or \
                    sorted_node_list[i]['id'] != secondary_node_list[i]['id']:
                secondary_node_list = grouping(node_list.copy())
                share_node_list(secondary_node_list, my_node_id)
                break

        # ここにそれ以降の処理を書く　あんまりいい実装じゃない


def _init_connect_network():
    global my_node_id
    print('/*----init_connect_network----*/')
    my_ip = None
    try:
        my_ip = ifaddresses('en0')[AF_INET][0]['addr']
    except ValueError:
        my_ip = ifaddresses('eth0')[AF_INET][0]['addr']
    finally:
        request_ip = input('request_ip:')
        res = throw_add_request(my_node_id, node_list, request_ip, my_ip)
        if res is False:
            # もし他のノードが存在しなかった時
            pre_node_list = create_node_list(my_node_id)
        else:
            # resの値をnode_listへ
            pre_node_list = res['node_list']

    return pre_node_list


if __name__ == '__main__':
    main()
