import time
import math


def grouping(node_list):
    print('**** groping.grouping ****')
    # ここを検証の際に変更する
    group_num = 3

    sorted_node_list = _boot_time_upper_sort(node_list)

    grouped_node_list = []
    node_list_length = len(sorted_node_list)

    # node数がgroup_num以下ならgroup_idが1になる
    if node_list_length < group_num:
        for i in range(node_list_length):
            sorted_node_list[0]['group_id'] = i + 1
            grouped_node_list.append(sorted_node_list.pop(0))

    else:
        for i in range(group_num):
            flag = True
            for j in range(int(node_list_length / group_num)):
                # popで取り出してgrouped_node_listに入れる

                if flag:
                    flag = False

                    sorted_node_list[0]['group_id'] = i + 1
                    grouped_node_list.append(sorted_node_list.pop(0))
                else:
                    flag = True
                    sorted_node_list[-1]['group_id'] = i + 1
                    grouped_node_list.append(sorted_node_list.pop(-1))

        last_node_groups_count = node_list_length % group_num

        if last_node_groups_count > 0:
            flag = True
            for k in range(last_node_groups_count):
                if flag:
                    flag = False
                    sorted_node_list[0]['group_id'] = group_num
                    grouped_node_list.append(sorted_node_list.pop(0))
                else:
                    flag = True
                    sorted_node_list[-1]['group_id'] = group_num
                    grouped_node_list.append(sorted_node_list.pop(-1))

    grouped_node_list = _boot_time_upper_sort(grouped_node_list)
    print(grouped_node_list)
    return grouped_node_list
    # TODO: node_listにgroup_idを書き込む
    # この処理の後ハートビートの処理を書く


def _boot_time_upper_sort(node_list: list):
    # boot_time(起動した日時)が最新のほうが上になるようにソート
    if len(node_list) <= 1:
        time.sleep(1)
    return sorted(node_list, key=lambda x: x['boot_time'], reverse=True)
