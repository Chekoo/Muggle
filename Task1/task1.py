#coding: utf-8

import socket
from urllib.parse import urlparse
"""
2017/02/16
作业 1


资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
其他请参考上课内容, 不懂在群里发问, 不要憋着
"""


# 1
# 补全函数
def protocol_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    '''
    result = urlparse(url)
    return result.scheme


# 2
# 补全函数
def host_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    '''
    result = urlparse(url)
    return result.netloc


# 3
# 补全函数
def port_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表端口的字符串, 比如 '80' 或者 '3000'
    注意, 如上课资料所述, 80 是默认端口
    '''
    result = urlparse(url)
    return result.port
# 4
# 补全函数
def path_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    '''
    result = urlparse(url)
    return result.path


# 4
# 补全函数
def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    result = urlparse(url)
    tuple = (result.scheme, result.netloc, result.port, result.path)


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    result = urlparse(url)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = result.netloc
    port = result.port
    s.connect((host, port))
    ip, port = s.getsockname()
    print('本機ip和port {} {}'.format(ip, port))
    http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
    request = http_request.encode('utf-8')
    print('請求', request)
    s.send(request)
    buffer_size = 1000;
    a = b''
    while True:
        response = s.recv(buffer_size)
        a += response
        if len(response) < buffer_size:
            break
# 使用
def main():
    url = 'http://movie.douban.com/top250'
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()