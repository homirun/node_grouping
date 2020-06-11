from netifaces import interfaces, ifaddresses, AF_INET


class NodeList:
    def __init__(self):
        #self._add_my_node()
        self._add_my_node()

    def add_node(self):
        pass

    def _add_my_node(self):
        # print(netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'])
        my_ip = ifaddresses('en0')[AF_INET][0]['addr']
        print(my_ip)
        my_node = Node(my_ip)
        print(my_node)


class Node:
    def __init__(self, ip):
        self.ip = ip
        self.group_id = None
        self.is_primary = False

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

