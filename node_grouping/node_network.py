import requests
import json
from flask import Flask, request
from node_grouping.node_list import NodeEncoder, create_node_id, Node
app = Flask(__name__)
node_list = dict()


# 待受側
@app.route('/api/add_request', methods=['post'])
def get_add_request():
    global node_list
    print('/*----get_add_request----*/')
    request_data = request.get_data()
    print(request_data)
    request_obj = json.loads(request_data)
    add_node_obj = Node(ip=request_obj['sender_ip'])
    node_id = create_node_id()
    node_list.update({str(node_id): add_node_obj})
    return json.dumps({'status': 200, 'response': 'request_response', 'node_list': node_list}, cls=NodeEncoder)


def start_api_server(nodes):
    print('/*----start_api_server---*/')
    global node_list
    node_list = nodes
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)


# 送信側
def throw_add_request(nodes, request_ip, my_ip):
    # up_timeを追加するかも
    print('/*----throw_add_request----*/')
    try:
        request_url = 'http://' + request_ip + '/api/add_request'
        res = requests.post(request_url,
                            json.dumps({'type': 'add_request', 'sender_ip': my_ip}),
                            headers={'Content-Type': 'application/json'})
        res = res.json()

        if res['response'] == 'request_response' and res['status'] == 200:
            print('OK: add request')
            print(res)

    except requests.exceptions.RequestException as e:
        print(e)
        return False

    return res
