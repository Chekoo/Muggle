import socket


def log(*args, **kwargs):
    # 用这个log代替print
    print('log', *args, **kwargs)


def route_index():
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')
    # 主頁的處理函數，返回主頁響應


def route_image():
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def error(code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',

    }
    return e.get(code, b'')

def response_for_path(path):
    '''
    根據path調用相應的處理函數
    沒有處理的path會返回404
    '''
    r = {
        '/': route_index,
        '/doge.gif': route_image,
    }
    response = r.get(path, error)
    return response()

def run(host='', port=3000):
    '''
    啟動服務器
    初始化socket套路，使用with可以保證
    程序中斷的時候正確關閉socket釋放佔用的端口
    '''
    with socket.socket() as s:
        # 連接
        s.bind((host, port))
        # 無限循環來處理請求
        while True:
            # 監聽 接受 讀取請求數據，解碼成字符串
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                # 因为 chrome 会发送空请求导致 split 得到空 list
                # 所以这里用 try 防止程序崩溃
                path = request.split()[1]
                # 用 response_for_path 函数来得到 path 对应的响应内容
                response = response_for_path(path)
                # 把響應發送給客戶端
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            # 處理結束，關閉連接
            connection.close()

if __name__ == '__main__':
    config = dict(
        host = '',
        port = 3000,
    )
    run(**config)