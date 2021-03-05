import socket
import os
from queue import Queue
from threading import Thread

HOST = '127.0.0.1'
PORT = 65432

class ThreadPoolManger():
    """线程池管理器"""
    def __init__(self, thread_num):
        # 初始化参数
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        # 初始化线程池，创建指定数量的线程池
        for i in range(thread_num):
            thread = ThreadManger(self.work_queue, i)
            thread.start()

    def add_job(self, func, *args):
        # 将任务放入队列，等待线程池阻塞读取，参数是被执行的函数和函数的参数
        self.work_queue.put((func, args))

class ThreadManger(Thread):
    """定义线程类，继承threading.Thread"""
    def __init__(self, work_queue, i):
        Thread.__init__(self)
        self.work_queue = work_queue
        self.daemon = True
        self.number = i

    def run(self):
        # 启动线程
        while True:
            target, args = self.work_queue.get()
            target(*args)
            print("thread number:" + str(self.number))
            self.work_queue.task_done()

# 创建一个有4个线程的线程池
thread_pool = ThreadPoolManger(4)

# 处理请求
def handleRequest(conn):

    directory = str(getDirectory("Xiaoaojianghu"))
    conn.send(directory.encode())       # 发送目录,即每章对应的页数

    data2 = conn.recv(1024)     # 接收客户端发送的阅读请求,包含章节和页面号
    print(data2)
    data2 = data2.decode()
    chapterNumber = data2.split("\r\n")[1].split(":")[1]
    pageNumber = data2.split("\r\n")[2].split(":")[1]

    fo = open(getFilenames("Xiaoaojianghu")[int(chapterNumber) - 1], "r")    # 根据章号和页号设置文件对象
    str1 = fo.read()     # 将txt文件内容读入到字符串str1中
    fo.close()
    if ((int(pageNumber) - 1) * 2048 > len(str1)):      # 处理越界情况,实际上客户端可确保不会出现这种情况
        conn.send('已越界'.encode())
    else:
        content = str1[2048 * (int(pageNumber) - 1):2048 * int(pageNumber)]     # 发送正确的小说内容
        content = content.encode('gb18030')
        conn.send(content)

# 读取文件夹中所有文件名
def getFilenames(dir_name):
    namelist = []
    for root, dirs, files in os.walk(dir_name):
        for filename in files:
            namelist.append(os.path.join(root, filename))
    return namelist

# 计算,即每章对应的页数
def getDirectory(dir_name):
    dir = {}
    i = 1
    namelist = getFilenames(dir_name)
    for f in namelist:
        fo = open(f, "r")
        cont = fo.read()
        dir[i] = int(len(cont)/2048) + 1    # 根据字数计算文件页数
        i = i + 1
    return dir

if __name__=='__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            connection, address = s.accept()
            thread_pool.add_job(handleRequest, *(connection,))