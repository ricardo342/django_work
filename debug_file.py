# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: debug_file
@time:2022/10/17
@Author:majiaqin 170479
@Desc:代码调试文件
'''

import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1> from test_file </h1>'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sun, 27 may 2018 01:01:01 GMT',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Length: {0}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)

def handle_connection(conn, addr):
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(2014)
    print(request)
    '''response转为bytes后传输'''
    conn.send(response.encode())
    conn.close()

def main():
    # socket.AF_INET用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM用于基于TCP的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用, 保证我们每次按Ctrl+C组合键之后，快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    # 设置backlog-socket连接最大排队数量
    serversocket.listen(5)
    print('http://127.0.0.1:8000')

    try:
        while True:
            conn, address = serversocket.accept()
            handle_connection(conn, address)
    except:
        pass
    finally:
        serversocket.close()
    pass

if __name__ == '__main__':
    pass