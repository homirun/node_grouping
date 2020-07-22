import requests
import json
import uptime
from flask import Flask, request
from node_grouping.node_list import *
app = Flask(__name__)
node_list = list()


# 待受側
@app.route('/api/add_request', methods=['post'])
def add_request():
    global node_list
    print('/*----get_add_request----*/')
    request_data = request.get_data()
    print(request_data)
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
    print(request_obj)
    node_list.clear()
    node_list.extend(request_obj['node_list'])
    # TODO:node_listの参照先を変えずにどうにかする方法を探す
    return json.dumps({'status': 200, 'response': 'request_response'}, cls=NodeEncoder)


def start_api_server(nodes):
    print('/*----start_api_server---*/')
    global node_list
    node_list = nodes
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)


def share_node_list(nodes, my_node_id):
    # この処理はPrimary決定時にグローバルとして自分がPrimaryであるかどうかを保持したほうがいいかもしれない
    my_group_id = get_my_group_id(nodes, my_node_id)
    is_primary = get_is_primary(nodes, my_node_id)
    my_group_node_list = get_my_group_node_list(nodes, my_group_id)
    destination_ip_list = list()
    if is_primary is True:
        print('**** list_share: primary *****')
        # 他のprimaryへ
        for i in nodes:
            if i['is_primary'] is True and i['id'] != my_node_id:
                destination_ip_list.append(i['ip'])

        # 自グループの一般ノードへ
        for i in my_group_node_list:
            if i['is_primary'] is False:
                destination_ip_list.append(i['ip'])
                break

    else:
        # 自分がPrimaryではないとき自グループのprimaryへ
        print('**** list_share: normal *****')
        for i in my_group_node_list:
            if i['is_primary'] is True:
                destination_ip_list.append(i['ip'])
                break

    print('destination_ip_list:')
    print(destination_ip_list)

    # TODO: portを固定するかどうか決める
    api_port = ':5000'

    for i in destination_ip_list:
        request_url = 'http://' + i + api_port + '/api/renew_node_list'
        res = requests.post(request_url,
                            json.dumps({'type': 'node_list_share', 'node_list': nodes}),
                            headers={'Content-Type': 'application/json'})
        res = res.json()
        print(res)


# 送信側
def throw_add_request(my_node_id, nodes, request_ip, my_ip):
    # up_timeを追加するかも
    print('/*----throw_add_request----*/')

    try:
        request_url = 'http://' + request_ip + '/api/add_request'

        res = requests.post(request_url,
                            json.dumps({'type': 'add_request', 'id': my_node_id,
                                        'sender_ip': my_ip, 'boot_time': get_boot_unix_time()}),
                            headers={'Content-Type': 'application/json'})
        res = res.json()

        if res['response'] == 'request_response' and res['status'] == 200:
            print('OK: add request')
            print(res)

    except requests.exceptions.RequestException as e:
        print(e)
        return False

    return res
