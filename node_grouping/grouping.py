import time
import math


def grouping(node_list):
    print('**** groping.grouping ****')
    # ここを検証の際に変更する
    group_num = 3

    sorted_node_list = _boot_time_upper_sort(node_list)

    grouped_node_list = []
    print(sorted_node_list)
    for i in range(group_num):
        for j in range(len(sorted_node_list) % group_num):
            # popで取り出してgrouped_node_listに入れる
            flag = True
            if flag:
                flag = False
                # sorted_node_list[0]
                grouped_node_list.append(sorted_node_list.pop(0))
                # sorted_node_list[0]
            else:
                flag = True
                grouped_node_list.append(sorted_node_list.pop(-1))

    # TODO: node_listにgroup_idを書き込む
    # この処理の後ハートビートの処理を書く


def _boot_time_upper_sort(node_list: dict):
    # boot_time(起動した日時)が最新のほうが上になるようにソート
    # TODO: すべてのnodelistをdict in listにする
    if len(node_list) <= 1:
        time.sleep(1)
    return sorted(node_list, key=lambda x: x['boot_time'], reverse=True)
