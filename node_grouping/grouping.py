
def grouping(node_list):
    print('**** groping.grouping ****')
    # ここを検証の際に変更する
    group_num = 3

    print(node_list)

    sorted_node_list = _boot_time_upper_sort(node_list)
    print(sorted_node_list)


def _boot_time_upper_sort(node_list: dict):
    # boot_time(起動した日時)が最新のほうが上になるようにソート
    return sorted(node_list.items(), key=lambda x: x[1]['boot_time'], reverse=True)

