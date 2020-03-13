#!/usr/bin/env python
# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler, HTTPServer
from wsgiref.simple_server import WSGIServer
import socket
import sys
from io import StringIO
#from app import application
from datetime import datetime
import threading

def application(env, start_response):
    s = env['PATH_INFO']
    start_response('200 OK', [('Content-Type', 'text/html'), ('X-Coder', 'Cooffeeli')])
    return ['<h1>'+s+'你好！！世界</h1>']

class WSGIServer_local(WSGIServer):

    def __init__(self, server_address):
        """初始构造函数, 创建监听socket"""
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.bind(server_address)
        self.listen_sock.listen(5)
        (host, port) = self.listen_sock.getsockname()
        self.server_port = port
        self.server_name = socket.getfqdn(host)
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False

    def set_application(self, application):
        """设置wsgi application, 供server 调用"""
        self.application = application

    def get_environ(self):
        """构造WSGI环境变量，传给application的env参数"""
        self.env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.request_method,
            'PATH_INFO': self.request_path,
            'SERVER_NAME': self.server_name,
            'SERVER_PORT': str(self.server_port),
            'wsgi.input': StringIO(str(self.request_data,encoding='utf-8')),
        }
        return self.env

    def start_response(self, http_status, http_headers):
        """构造WSGI响应， 传给application的start_response"""
        self.http_status = http_status
        self.http_headers = dict(http_headers)
        headers = {
            'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': 'WSGIServer 1.0'
        }
        self.http_headers.update(headers)

    def parse_request(self, text):
        """获取http头信息，用于构造env参数"""
        request_line = text.splitlines()[0]
        request_line = str(request_line,encoding='utf-8')
        print("request_line=%s"%request_line)
        request_info = request_line.split(' ')
        (self.request_method,
         self.request_path,
         self.request_version) = request_info

    def get_http_response(self, response_data):
        """完成response 内容"""
        res = 'HTTP/1.1 {status} \r\n'.format(status=self.http_status)
        for header in self.http_headers.items():
            res += '{0}: {1} \r\n'.format(*header)

        res += '\r\n'

        res_body = ''
        for val in response_data:
            res_body += val

        res += res_body

        return res

    def handle_request(self):
        """处理请求"""
        # 初始版本，只接受一个请求
        conn, addr = self.listen_sock.accept()

        # 获取http 请求的request内容
        self.request_data = conn.recv(1024)
        self.parse_request(self.request_data)

        # 构造调用application需要的两个参数 env, start_response
        env = self.get_environ()
        start_response = self.start_response

        # 调用application, 并获取需要返回的http response内容
        response_data = self.application(env, start_response)

        # 获取完整http response header 和 body, 通过socket的sendall返回到客户端
        res = self.get_http_response(response_data)
        conn.sendall(str.encode(res))

        # 脚本运行完毕也会结束
        conn.close()

    def serve_forever(self):
        super().serve_forever()
def make_server(server_address, application):
    """创建WSGI Server 负责监听端口，接受请求"""
    wsgi_server = WSGIServer_local(server_address)
    wsgi_server.set_application(application)

    return wsgi_server


SERVER_ADDRESS = (HOST, PORT) = '', 8001
wsgi_server = make_server(SERVER_ADDRESS, application)
wsgi_server.handle_request()
wsgi_server.serve_forever()