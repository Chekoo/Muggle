"""
url 的规范
第一个 ? 之前的是 path
? 之后的是 query
http://c.cc/search?a=b&c=d&e=1
PATH  /search
QUERY a=b&c=d&e=1
"""

import socket
import urllib.parse
from utils import log
from routes import route_static
from routes import route_dict

# 定义一个class用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''


    def form(self):
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def error(request, code=404):
    '''根据code返回不同的错误响应'''
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    # 解析路径以字典形式返回
    """
    message=hello&author=gua
    {
        'message': 'hello',
        'author': 'gua',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据path调用相应的处理函数
    没有处理的path会返回404
    """
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    '''启动服务器'''
    # 初始化socket套路
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            r = connection.recv(1000)
            r = r.decode('utf-8')
            # log('ip and request, {}\n{}'.format(address, request))
            # 因为 chrome 会发送空请求导致 split 得到空 list
            # 所以这里判断一下防止程序崩溃
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 设置request的method
            request.method = r.split()[0]
            # 把body放入request中
            request.body = r.split('\r\n\r\n', 1)[1]
            # 用response_for_path函数来得到path对应内容
            response = response_for_path(path)
            # 把响应发给客户端
            connection.sendall(response)
            # 关闭
            connection.close()


if __name__ == '__main__':
    config = dict(
        host = '',
        port = 3000,
    )
    run(**config)