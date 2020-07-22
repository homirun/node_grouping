import requests
import json
import uptime
from flask import Flask, request
from node_grouping.node_list import NodeEncoder, create_node_id, Node, get_boot_unix_time
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
    # node_list.clear()
    # node_list.append(request_obj)
    # TODO:node_listの参照先を変えずにどうにかする方法を探す


def start_api_server(nodes):
    print('/*----start_api_server---*/')
    global node_list
    node_list = nodes
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)


def node_list_share(nodes, my_node_id):
    # この処理はPrimary決定時にグローバルとして自分がPrimaryであるかどうかを保持したほうがいいかもしれない
    is_primary = False
    for i in nodes:
        if i['id'] == my_node_id and i['is_primary'] is True:
            # 自分がPrimary
            is_primary = True
            break
        else:
            pass
    if is_primary is False:
        # Primaryでないとき
        pass
    pass


# 送信側
def throw_add_request(nodes, request_ip, my_ip):
    # up_timeを追加するかも
    print('/*----throw_add_request----*/')

    try:
        request_url = 'http://' + request_ip + '/api/add_request'
        node_id = create_node_id()
        res = requests.post(request_url,
                            json.dumps({'type': 'add_request', 'id': node_id,
                                        'sender_ip': my_ip, 'boot_time': get_boot_unix_time()}),
                            headers={'Content-Type': 'application/json'})
        res = res.json()

        if res['response'] == 'request_response' and res['status'] == 200:
            print('OK: add request')
            print(res)

    except requests.exceptions.RequestException as e:
        print(e)
        return False, None

    return res, node_id
