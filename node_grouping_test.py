from node_grouping.node_network import *
from node_grouping.node_list import *
from node_grouping.grouping import *
import os
import threading
import json
from multiprocessing import Value, Manager

import time
import logging
import sys


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')
node_list = list()
secondary_node_list = list()
my_node_id = None


def main():
    global node_list, secondary_node_list, my_node_id
    print('/*----main----*/')
    my_node_id = create_node_id()
    api_server_thread = threading.Thread(target=start_api_server, args=[node_list, my_node_id], name='api_server')
    # api_server_thread.setDaemon(True)
    api_server_thread.start()
    node_list = _init_connect_network(node_list)
    # TODO:APIサーバがあがる前にgroupingを始めるとノード変更通知を送信できないノードが出てくるので暫定的処理
    time.sleep(3)
    # nodelistに更新があったらグルーピングを行う copyは値渡し

    # grouping(node_list.copy())
    secondary_node_list = None
    while True:
        # time.sleep(3)
        # print('prime:')
        # print(node_list)
        # print('second:')
        # print(secondary_node_list)
        # print('id:')
        # print(id(node_list))
        is_for_primary = False
        sender_ip = None

        tmp_node_list = node_list.copy()

        if 'for_primary' in tmp_node_list:
            is_for_primary = True
            tmp_node_list.remove('for_primary')
            node_list.remove('for_primary')
            for i in tmp_node_list:
                if 'sender_ip' in i:
                    sender_ip = i['sender_ip']
                    meta_index = [d.get('sender_ip') for d in node_list]
                    for j in range(len(meta_index)):
                        if meta_index[j] is not None:
                            del node_list[j]
                            break
                    tmp_node_list.remove(i)
                    break
            # print('tmp')
            # print(tmp_node_list)
            # print('node')
            # print(node_list)

        # secondary_node_listにfor_primaryが一番最初の処理で入らないように
        # secondary_node_listはold_node_listのほうが名前が的確かもしれない
        # TODO: node追加がwhileを一周する前に複数来ると配布がうまくいかなくなる.
        if secondary_node_list is None:
            secondary_node_list = tmp_node_list
            grouping(tmp_node_list)

        sorted_node_list = node_id_upper_sort(tmp_node_list)
        sorted_secondary_node_list = node_id_upper_sort(secondary_node_list)
        for i in range(len(sorted_node_list)):
            # print(i)
            if len(sorted_node_list) != len(sorted_secondary_node_list) or \
                    sorted_node_list[i]['id'] != sorted_secondary_node_list[i]['id']:
                sorted_node_list = grouping(sorted_node_list.copy())
                share_node_list(sorted_node_list.copy(), sorted_secondary_node_list.copy(), sender_ip,  my_node_id, is_for_primary)
                secondary_node_list = sorted_node_list
                break

        # ここにそれ以降の処理を書く　あんまりいい実装じゃない


def _init_connect_network(nodes: list):
    global my_node_id
    print('/*----init_connect_network----*/')
    my_ip = None
    try:
        my_ip = ifaddresses('en0')[AF_INET][0]['addr']
    except ValueError:
        my_ip = ifaddresses('eth0')[AF_INET][0]['addr']
    finally:
        args = sys.argv
        if len(args) > 1:
            request_ip = args[1]
        else:
            request_ip = input('request_ip:')
        res = throw_add_request(my_node_id, node_list, request_ip, my_ip)
        if res is False:
            # もし他のノードが存在しなかった時
            nodes.extend(create_node_list(my_node_id))
        else:
            # resの値をnode_listへ
            nodes.extend(res['node_list'])
    return nodes


if __name__ == '__main__':
    main()
