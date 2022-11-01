# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: debug_file
@time:2022/10/17
@Author:majiaqin 170479
@Desc:代码调试文件
'''

import os
import sys
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

def Repsonse(*args, **kwargs):
    pass

'''简单的web application程序'''
def simple_app(environ, start_response):
    """Simplest possible application object"""
    # status = '200 OK'
    # response_headers = [('Content-type', 'text/plain')]
    # start_response(status, response_headers)
    # return [b'Hello world! -by the5fire \n']
    '''直接封装response对象'''
    response = Repsonse('Hello World', start_response=start_response)
    # 这个函数里面调用start_response
    response.set_header('Content-Type', 'text/plain')
    return response

'''编写可以调用simple_app方法的程序'''
def wsgi_to_bytes(s):
    return s.encode()

def run_with_cgi(application):
    environ = dict(os.environ.items())
    environ['wsgi.input'] = sys.stdin.buffer
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once'] = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        out = sys.stdout.buffer

        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # 在输出第一行数据之前, 先发送响应头
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes('Status: {0}\r\n'.format(status)))
            for header in response_headers:
                out.write(wsgi_to_bytes('{0}: {0}\r\n'.format(header)))
            out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()

    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # 如果已经发送了header, 则重新抛出原始异常信息
                    raise (exc_info[0], exc_info[1], exc_info[2])
            finally:
                # 避免循环引用
                exc_info = None
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]
        return write
    result = application(environ, start_response)

    try:
        for data in result:
            # 如果没有body数据, 则不发送header
            if data:
                write(data)
        if not headers_sent:
            # 如果body数据为空, 则发送数据header
            write('')
    finally:
        if hasattr(result, 'close'):
            result.close()

class AppClass(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __call__(self, environ, start_response):
        print(environ, start_response)
        start_response(self.status, self.response_headers)
        return [b'Hello AppClass.__call__\n']

application = AppClass()

class AppClassIter(object):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        self.start_response(self.status, self.response_headers)
        yield b'Hello AppClassIter\n'

def set_status(status=None):
    pass

def set_header(*args):
    pass

def start_response(status, headers):
    # 伪代码
    set_status(status)
    for k, v in headers:
        set_header(k, v)

def handle_conn(conn, environ, start_response):
    # 调用前面定义的application
    app = application(environ, start_response)
    # 遍历返回的结果，生成response
    response = ''
    for data in app:
        response += data

    conn.sendall(response)

if __name__ == '__main__':
    run_with_cgi(simple_app)
    pass