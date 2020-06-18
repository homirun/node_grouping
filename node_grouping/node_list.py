from netifaces import interfaces, ifaddresses, AF_INET
import uuid


class NodeList(dict):
    def __init__(self):
        super().__init__()
        self.node_id = None
        self.node = None

    def add_node(self):
        pass

    def add_my_node(self):
        # 自分のIPは初回の依頼の返信時に教えてもらうほうがいいかもしれない(1台目は無理なので手動？)
        # print(netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])
        self.node_id = uuid.uuid4()
        my_ip = ifaddresses('en0')[AF_INET][0]['addr']
        my_node = Node(my_ip)
        self.node = my_node


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

    def set_primary_status(self, is_primary:bool):
        self.is_primary = is_primary

    def get_primary_status(self):
        return self.is_primary


if __name__ == '__main__':
    n = NodeList()

