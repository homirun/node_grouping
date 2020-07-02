from netifaces import interfaces, ifaddresses, AF_INET
import uuid
import json


# class NodeList(dict):
#     def __init__(self):
#         super().__init__()
#         self.node_id = None
#         self.node = None
#
#     def add_node(self):
#         pass
#
#     def add_my_node(self):
#         # 自分のIPは初回の依頼の返信時に教えてもらうほうがいいかもしれない(1台目は無理なので手動？)
#         # print(netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])
#         self.node_id = uuid.uuid4()
#         my_ip = None
#         try:
#             my_ip = ifaddresses('en0')[AF_INET][0]['addr']
#         except ValueError:
#             my_ip = ifaddresses('eth0')[AF_INET][0]['addr']
#         finally:
#             my_node = Node(my_ip)
#             self.node = my_node


class Node:
    def __init__(self, ip, group_id=None, is_primary=False, is_me=False):
        self.ip = ip
        self.group_id = group_id
        self.is_primary = is_primary
        self.is_me = is_me

    def set_ip(self, ip):
        self.ip = ip

    def get_ip(self):
        return self.ip

    def set_group(self, group_id):
        self.group_id = group_id

    def get_group(self):
        pass

    def set_primary_status(self, is_primary: bool):
        self.is_primary = is_primary

    def get_primary_status(self):
        return self.is_primary


class NodeEncoder(json.JSONEncoder):
    def default(self, o):
        print(o)
        if isinstance(o, Node):
            return o.__dict__
        elif isinstance(o, object):
            return o.__dict__
        else:
            raise TypeError


def create_node_list():
    with open('./node_list', mode='w') as f:
        node_id = create_node_id()
        my_ip = None
        try:
            my_ip = ifaddresses('en0')[AF_INET][0]['addr']
        except ValueError:
            my_ip = ifaddresses('eth0')[AF_INET][0]['addr']
        finally:
            my_node = Node(my_ip)

        pre_node_list = dict({str(node_id): my_node.__dict__})

    return pre_node_list


def create_node_id():
    return uuid.uuid4()
