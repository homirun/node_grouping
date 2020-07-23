import requests
import json
import uptime
from flask import Flask, request
from node_grouping.node_list import *
app = Flask(__name__)
node_list = list()
my_node_id = None
latest_time_stamp = 0


# 待受側
@app.route('/api/add_request', methods=['post'])
def add_request():
    global node_list
    print('/*----add_request----*/')
    request_data = request.get_data()
    # print(request_data)
    request_obj = json.loads(request_data)
    # node_id = create_node_id()
    add_node_obj = Node(uid=request_obj['id'], ip=request_obj['sender_ip'], boot_time=request_obj['boot_time'])
    node_list.append(add_node_obj.__dict__)
    # print('api_node_list_id:')
    # print(id(node_list))
    return json.dumps({'status': 200, 'response': 'request_response', 'node_list': node_list}, cls=NodeEncoder)


@app.route('/api/renew_node_list', methods=['post'])
def renew_node_list():
    request_data = request.get_data()
    request_obj = json.loads(request_data)
    my_group_id = get_my_group_id(node_list, my_node_id)
    is_primary = get_is_primary(node_list, my_node_id)

    # print(request_obj)
    node_list.clear()
    node_list.extend(request_obj['node_list'])
    if request_obj['for_primary']:
        node_list.append({'sender_ip': request.remote_addr})
        node_list.append('for_primary')
    return json.dumps({'status': 200, 'response': 'request_response'}, cls=NodeEncoder)
    # else:
    #     return json.dumps({'status': 500, 'response': 'Error: old time_stamp'}, cls=NodeEncoder)


def start_api_server(nodes, my_id):
    print('/*----start_api_server---*/')
    global node_list, my_node_id
    node_list = nodes
    my_node_id = my_id
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)


def share_node_list(nodes, old_nodes, sender_ip, my_id, is_for_primary):
    # この処理はPrimary決定時にグローバルとして自分がPrimaryであるかどうかを保持したほうがいいかもしれない
    my_group_id = get_my_group_id(nodes, my_id)
    is_primary = get_is_primary(nodes, my_id)
    old_my_group_node_list = get_my_group_node_list(old_nodes, my_group_id)
    destination_ip_list = list()
    if is_primary is True:
        print('**** list_share: primary *****')
        # 他のprimaryへ
        # 他のprimaryから来た更新で無いならば
        for i in old_nodes:
            if i['is_primary'] is True and i['id'] != my_id and i['ip'] != sender_ip:
                destination_ip_list.append(i['ip'])

        # 自グループの一般ノードへ
        for i in old_my_group_node_list:
            if i['is_primary'] is False and i['ip'] != sender_ip:
                destination_ip_list.append(i['ip'])
                break

    else:
        # 自分がPrimaryではないとき自グループのprimaryへ
        print('**** list_share: normal *****')
        for i in old_my_group_node_list:
            if i['is_primary'] is True and i['ip'] != sender_ip:
                destination_ip_list.append(i['ip'])
                break


    print('destination_ip_list:')
    print(destination_ip_list)

    # TODO: portを固定するかどうか決める
    api_port = ':5000'

    for i in destination_ip_list:
        request_url = 'http://' + i + api_port + '/api/renew_node_list'
        res = requests.post(request_url,
                            json.dumps({'type': 'node_list_share', 'node_list': nodes, 'time_stamp': get_now_unix_time(), 'for_primary': is_primary}),
                            headers={'Content-Type': 'application/json'})
        res = res.json()
        print(res)


# 送信側
def throw_add_request(my_id, nodes, request_ip, my_ip):
    # up_timeを追加するかも
    print('/*----throw_add_request----*/')

    try:
        request_url = 'http://' + request_ip + '/api/add_request'

        res = requests.post(request_url,
                            json.dumps({'type': 'add_request', 'id': my_id,
                                        'sender_ip': my_ip, 'boot_time': get_boot_unix_time(),
                                        'time_stamp': get_now_unix_time()}),
                            headers={'Content-Type': 'application/json'})
        res = res.json()

        if res['response'] == 'request_response' and res['status'] == 200:
            print('OK: add request')
            print(res)

    except requests.exceptions.RequestException as e:
        print(e)
        return False

    return res
