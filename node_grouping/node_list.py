from netifaces import interfaces, ifaddresses, AF_INET
import uuid
import json
import uptime


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
    def __init__(self, uid, ip, boot_time, group_id=None, is_primary=False, is_me=False):
        self.id = uid
        self.ip = ip
        self.boot_time = boot_time
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
        if isinstance(o, Node):
            return o.__dict__
        elif isinstance(o, object) and hasattr(o, '__dict__'):
            return o.__dict__
        elif isinstance(o, object):
            return super(NodeEncoder, self).default(o)
        else:
            raise TypeError


def create_node_list():
    node_id = create_node_id()
    my_ip = None
    try:
        my_ip = ifaddresses('en0')[AF_INET][0]['addr']
    except ValueError:
        my_ip = ifaddresses('eth0')[AF_INET][0]['addr']
    finally:
        my_node = Node(uid=node_id, ip=my_ip, boot_time=get_boot_unix_time())

    pre_node_list = list()
    pre_node_list.append(my_node.__dict__)

    return pre_node_list


def create_node_id():
    return str(uuid.uuid4())


def get_boot_unix_time():
    return uptime.boottime().timestamp()


def get_my_group_id(nodes, my_id):
    my_group_id = None

    for i in nodes:
        if i['id'] == my_id:
            my_group_id = i['group_id']

    return my_group_id


def get_my_group_node_list(nodes, my_group_id):
    my_group_node_list = list()
    for i in nodes:
        if i['group_id'] == my_group_id:
            my_group_node_list.append(i)
    return my_group_node_list
