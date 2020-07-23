import time
import math


def grouping(node_list):
    print('**** groping.grouping ****')
    # ここを検証の際に変更する
    start_time = time.time()
    group_num = 3
    # print(node_list)
    sorted_node_list = boot_time_upper_sort(node_list)

    grouped_node_list = list()
    node_list_length = len(sorted_node_list)

    # node数がgroup_num以下の時の処理
    if node_list_length <= group_num:
        for i in range(node_list_length):
            # print(i)
            sorted_node_list[0]['group_id'] = i + 1
            sorted_node_list[0]['is_primary'] = True
            grouped_node_list.append(sorted_node_list.pop(0))

    else:
        for i in range(group_num - 1):
            local_grouped_list = list()
            flag = True
            for j in range(int(node_list_length / group_num)):
                # popで取り出してgrouped_node_listに入れる

                if flag:
                    flag = False
                    sorted_node_list[0]['is_primary'] = False
                    sorted_node_list[0]['group_id'] = i + 1
                    local_grouped_list.append(sorted_node_list.pop(0))
                else:
                    flag = True
                    sorted_node_list[-1]['is_primary'] = False
                    sorted_node_list[-1]['group_id'] = i + 1
                    local_grouped_list.append(sorted_node_list.pop(-1))
            # 何回もソートかけてるので直したい
            local_grouped_list = boot_time_upper_sort(local_grouped_list)
            local_grouped_list[-1]['is_primary'] = True
            grouped_node_list.extend(local_grouped_list)

        last_node_groups_count = node_list_length % group_num

        # 最後のグループだけ端数のノードの処理があるため別
        # TODO: ここの処理のせいで5ノード3グループのときなどに[1,2,3,3,3]のようになってしまう

        local_grouped_list = list()
        flag = True
        for k in range(int(node_list_length / group_num) + last_node_groups_count):
            if flag:
                flag = False
                sorted_node_list[0]['is_primary'] = False
                sorted_node_list[0]['group_id'] = group_num
                local_grouped_list.append(sorted_node_list.pop(0))
            else:
                flag = True
                sorted_node_list[-1]['is_primary'] = False
                sorted_node_list[-1]['group_id'] = group_num
                local_grouped_list.append(sorted_node_list.pop(-1))

        local_grouped_list = boot_time_upper_sort(local_grouped_list)
        local_grouped_list[-1]['is_primary'] = True
        grouped_node_list.extend(local_grouped_list)

    grouped_node_list = boot_time_upper_sort(grouped_node_list)
    print(grouped_node_list)
    print('group_count:')
    print(len(grouped_node_list))

    end_time = time.time()
    run_time = end_time - start_time
    print(f'grouping 実行時間:{run_time}')
    return grouped_node_list

    # この処理の後ハートビートの処理を書く


def boot_time_upper_sort(node_list: list):
    # boot_time(起動した日時)が最新のほうが上になるようにソート
    if len(node_list) <= 1:
        time.sleep(1)
    return sorted(node_list, key=lambda x: x['boot_time'], reverse=True)


def node_id_upper_sort(node_list: list):
    if len(node_list) <= 1:
        time.sleep(1)
    return sorted(node_list, key=lambda x: x['id'], reverse=True)
