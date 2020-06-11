# これから稼働するノード
def init_node():
    if is_node_has_not_ip_list or is_list_during_response_has_node_not_exists
        running_node_ip = input('running_node_ip')
    else:
        running_node = connect(running_node_ip)
        running_node.add_node(MY_IP_ADDRESS)


# すでに稼働している方
## ip_list関連はdictのほうが良いかもしれない

# ip追加依頼　イベント化
@add_node
def add_node(add_node_ip:list):
    ip_list.append(add_node_ip)

    for address in primary_node_ips:
        primary_node = connect(address)
        primary_node.submit_list(ip_list)

# イベント化
@submit_list
def submit_list(add_ip_list:list):
    ip_list = add_ip_list


# grouping
def _grouping():
    if is_running_node_even:
        # ipアドレスを用いてグルーピング
        pass 
    else:
        # 何かしらの一意の識別子が必要
        affiliation_group = group.create(id=hash_number)
    
    group_primary_ip = _primary_election(affiliation_group.ips)


# リーダー選出   
def _primary_election(ip_list_in_groups=list, is_tmp_primary=False):

    return primary_ip


# 各Primaryの通知
def _notice_primary(is_tmp_primary=False):
    tmp_ip_list = []

    for i in primary_node_count:
        once_ip_list = list(set(tmp_ip_list) - set(ip_list))
        tmp_node = connect(once_ip_list[random(once_ip_list.conunt)])

        if tmp_node.status != 'primary':
            primary_ip = tmp_node.primary.ip
            tmp_node = connect(primary_ip)
        
        tmp_ip_list.append(tmp_node.get_group_ip_list)


# 障害発生
def _start_failure:
    if is_network_partition:
        if primary_node_count / 2 > connecting_primary_node_count:
            shutdown()
    else:
        #故障したノードを停止 処理は未定
        pass
    
    if is_primary_disconnect:
        if MY_IP_ADDRESS == _primary_election(survival_node_ips):
            _notice_primary(is_tmp_primary=true)


def main():
    init_node()


#########################################

# while True:
#
#     if ノードを追加する or 復旧したノードが存在する:
#
#         if 復旧したノードが障害発生前に保持していたIPリストが存在していない or リストの中に応答があるノードが存在しない:
#                 現在稼働しているノードのIPを手動で設定する
#
#         設定したIPのノードに接続してIPリストに追加させる
#         PrimaryもしくはTemporaryPrimaryを経由してIPリストを配布する
#
#     if 現状稼働しているノードが偶数:
#         ノードをグループ数が奇数になるようにグルーピングする
#     else:
#         それぞれ1台のみでグルーピングする
#
#     リーダ選出アルゴリズムでPrimaryノードを各グループ内で1つ選出する
#
#
#     # 各Primaryの通知
#     for i in range(Primaryノード数):
#
#         自分のグループとTemporaryIPリスト以外の適当なノードへ「属しているグループのPrimaryノードのIP」を問い合わせる
#         結果をTemporaryIPリストに追記する
#
#         if 問い合わせた先がPrimaryノードだった:
#             そのグループ内のノードのIPを問い合わせる
#         else:
#             手に入れた別グループのPrimaryノードIPへそのグループ内の全てのノードのIPを問い合わせる
#             結果をTemporaryIPリストに追記する
#
#
#     # 障害発生
#     if 障害が発生している:
#
#         if ノード単体の故障ではなくネットワーク分断により応答がない:
#             生存Primary数の少ない方のノードを全て停止する
#         else:
#             故障したノードを停止
#
#         if 停止したノードの中にPrimaryノードが含まれていた:
#             Primaryが存在しないグループ内でTemporaryPrimaryを選出してその他各Primaryに通知
#
#
