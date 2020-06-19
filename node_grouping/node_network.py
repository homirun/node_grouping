import requests
import json
from flask import Flask, request
from multiprocessing import Pool
from node_grouping_test import notified_add_request
import time
app = Flask(__name__)


# 待受側
@app.route('/api/add_request', methods=['post'])
def get_add_request():
    print('/*----get_add_request----*/')
    request_data = request.get_data()
    print(request_data)
    print('fires')
    notified_add_request(request_data)
    time.sleep(5)

    return json.dumps({'status': 200, 'response': 'request_response', 'node_list': {'hoge': 'fuga'}})


def start_api_server():
    print('/*----start_api_server---*/')
    app.run('0.0.0.0', port=5000, debug=True, use_reloader=False)


# 送信側
def throw_add_request(node_list, request_ip, my_ip):
    # up_timeを追加するかも
    print('/*----throw_add_request----*/')
    try:
        request_url = 'http://' + request_ip + '/api/add_request'
        print(request_url)
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
