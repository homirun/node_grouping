import requests
import json
from flask import Flask, request
from multiprocessing import Pool

app = Flask(__name__)


# 待受側
@app.route('/api/add_request', methods=['post'])
def get_add_request():
    print('/*----get_add_request----*/')
    request_data = request.get_data()
    print(request_data)


def start_api_server():
    print('/*----start_api_server---*/')
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)


# 送信側
def throw_add_request(node_list, request_ip, my_ip):
    # up_timeを追加するかも
    print('/*----throw_add_request----*/')
    try:
        res = requests.post('http://' + request_ip + '/api/add_request',
                            json.dumps({'type': 'add_request', 'sender_ip': my_ip}),
                            headers={'Content-Type': 'application/json'})
        res = json.loads(res.json())

        if res['type'] == 'request_response' and res['status'] == 200:
            pass

    except requests.exceptions.RequestException as e:
        print(e)
        return False

    return res
