
import socket
import ssl
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
    pass

# 2
# 补全函数
def host_of_url(url):
    pass



# 3
# 补全函数
def port_of_url(url):
    pass

# 4
# 补全函数
def path_of_url(url):
    pass



# 4
# 补全函数
def parsed_url(url):

    # 檢查協議
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # 檢查默认 path
    i = u.find('/')
    if i == -1:  # find找不到返回-1
        host = u
        path = '/'
    else:  # g.cn/hello
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }

    # 默认端口
    port = port_dict[protocol]
    if ':' in host:  # 若host里面有:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body

def socket_by_protocol(protocol):
    '''根据一个协议返回一个socket实例'''
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    '''
    参数是一个socket实例
    返回这个socket读取的所有数据
    '''
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def get(url):
    '''
    用GET请求url并返回响应
    '''
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)

    if status_code == 301:
        url = headers['Location']
        return get(url)

    return status_code, headers, body


# 使用
def main():
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    print(status_code, headers, body)


def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        # assert是一个语句，叫做断言，若条件成立，则通过测试
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'


def test_get():
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]
    for u in urls:
        get(u)


def test():
   test_parsed_url()
   test_get()
   test_parsed_response()

if __name__ == '__main__':
    test()
    main()