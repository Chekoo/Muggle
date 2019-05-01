import json

from .utils import log


def save(data, path):
    '''
    本函数把一个dict或者list写入文件
    data是dict或者list
    path 是保存文件的路径
    '''
    # json 是一个序列化/反序列化(上课会讲这两个名词) list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    '''
    本函数从一个文件中载入数据并转化为dict或list
    path是保存文件的路径
    '''
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)

# Model是用于存储数据的基类
class Model(object):
    # @classmethod说明这是一个类方法
    # 类方法的调用方式是 类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod有一个参数是class
        # 所以我们可以得到class的名字
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        '''得到一个类的所有存储的实例'''
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        '''save函数用于把一个Models的实例保存到文件中'''
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >'.format(classname, s)


# 类用于实际的数据处理
# 因为继承 Model
# 所以可以直接save load
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')

