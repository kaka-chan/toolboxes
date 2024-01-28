import socket


def get_ip_status(ip, port=80):
    """
    判断端口是否在线, 80端口默认都是开启的
    :param ip: 目标ip
    :param port: 目标端口
    :return: bool值
    """
    flag = False
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.settimeout(0.1)
    result = server.connect_ex((ip, port))
    if result == 0:
        flag = True
    server.close()
    return flag
