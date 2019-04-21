import time


def log(*args, **kwargs):
    # time.time()返回unix time
    # 如何把unix time 轉換為屁同人可以看懂的格式呢？
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)