import requests
import json


def throw_add_request(node_list, request_ip):
    # up_timeを追加するかも
    res = requests.post(request_ip,
                        json.dumps({'type': 'add_request', 'sender_ip': request_ip}),
                        headers={'Content-Type': 'application/json'})
    res = json.loads(res.json())

    if res['type'] == 'request_response' and res['status'] == 200 :
        pass
