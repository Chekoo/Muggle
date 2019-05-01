from .utils import log
from .models import Message
from .models import User


message_list = []


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    '''主页的处理函数，返回主页的响应'''
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf=8')


def route_login(request):
    header = 'HTTP/1.1 2100 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html'
    if request.method == 'POST':
        # HTTP BODY如下
        # username=gw123&password=123
        # 经过request.form()函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.formate(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        resutl = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    '''主页的处理函数，返回主页的响应'''
    log('本次请求的method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{message}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """静态资源的处理函数，读取图书并生成响应返回"""
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}