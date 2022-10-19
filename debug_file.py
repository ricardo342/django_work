# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: debug_file
@time:2022/10/17
@Author:majiaqin 170479
@Desc:代码调试文件
'''

import errno
import socket
import requests
import json
import threading
import pprint
import time

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello, world! <h1> from test_file (thread_name) </h1>'''
response_params = [
    'HTTP/1.0 200 OK',
    'Date: Sun, 27 may 2018 01:01:01 GMT',
    'Content-Type: text/plain; charset=utf-8',
    'Content-Length: {0}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)

def handle_connection(conn, addr):
    # print('oh, new conn', conn, addr)
    # time.sleep(100)
    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(2014)
    print(request)
    current_thread = threading.currentThread()
    content_length = len(body.format(thread_name=current_thread.name).encode())
    print(current_thread.name)
    '''response转为bytes后传输'''
    # conn.send(response.encode())
    conn.send(response.format(thread_name=current_thread.name, length=content_length).encode())
    conn.close()

def main():
    # socket.AF_INET用于服务器与服务器之间的网络通信
    # socket.SOCK_STREAM用于基于TCP的流式socket通信
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口可复用, 保证我们每次按Ctrl+C组合键之后，快速重启
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('127.0.0.1', 8000))
    # 设置backlog-socket连接最大排队数量
    serversocket.listen(10)
    print('http://127.0.0.1:8000')
    # 设置socket为非阻塞模式
    serversocket.setblocking(0)
    try:
        i = 0
        while True:
            try:
                conn, address = serversocket.accept()
                handle_connection(conn, address)
            except socket.error as e:
                if e.args[0] != errno.EAGAIN:
                    raise e
            continue
            i += 1
            print(i)
            t = threading.Thread(target=handle_connection, args=(conn, address),
                                 name='thread-{0}'.format(i))
            t.start()
    finally:
        serversocket.close()
    pass

def api_test():
    url = "http://alicloud.estonapi.top:8000/marketplace/messages/unread?user_id=698708461&mark_as_read=false&role=seller"
    header = {'Authorization': 'Bearer  APP_USR-7483778333791187-101902-30cc2f4e50379f7679478d7a883d5bab-698703218'}
    r = requests.get(url, headers=header)
    return r.json()

if __name__ == '__main__':
    # main()
    pprint.pprint(api_test())
    pass