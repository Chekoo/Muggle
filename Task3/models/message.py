from ..models import Model


# 定义一个class用于保存message
class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')