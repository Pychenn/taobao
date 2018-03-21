#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Subject：多线程测试建模-生产者消费者模型
Note：用生产者模型代替request请求模块，处理速度0.2s-0.5s
      用消费者模型代替正则解析模块，处理速度0.5s-0.8s
      如果模拟总共请求150个页面，用100个线程进行请求处理，20个线程进行解析处理，所需时间约5s（150*0.65/20）
      如果模拟总共请求150个页面，用100个线程进行请求处理，10个线程进行解析处理，所需时间约10s（150*0.65/10）
'''

import time
import threading
import queue
import random


def fun_1(name):
    while 1:
        i = url_queue.get(1)        #从url队列里拿取数据，进行相应处理
        time.sleep(random.uniform(0.2,0.5))     #模拟request处理操作
        html = random.randint(1,100)
        print("生产%s的数据：%s" % (i+1,html))
        html_queue.put(html,1)      #把生产好的数据放入html队列里
        print("生产后的队列size：%s"%html_queue.qsize())
        if url_queue.qsize() ==0:       #url队列为空，说明所有url请求完毕，生产线程关闭
            break

def fun_2():
    while 1:
        data = html_queue.get(1)        #从html队列里拿取数据，进行相应处理
        time.sleep(random.uniform(0.5,0.8))     #模拟re处理操作
        print("消费的数据：%s"%data)
        print("消费后的队列size：%s" % html_queue.qsize())
        if html_queue.qsize() ==0:      #html队列为空，说明所有生产好的html都处理完毕，消费线程关闭
            break


#main()函数，程序执行流程
def main():
    global url_queue
    url_queue = queue.Queue(1000)   #创建存放url的队列，最大值1000
    global html_queue
    html_queue = queue.Queue(500)   #创建存放html的队列，最大值500
    name = "男装"   #模拟传进去参数
    threads = []    #存放所有线程的队列

    print(time.ctime())
    for p in range(150):   #总共需要请求的页面数，创建url队列
        url_queue.put(p,1)

    for i in range(100):    #创建生产模块的线程，数量100个
        t = threading.Thread(target=fun_1,args=(name,))
        threads.append(t)

    for i in range(20):     #创建消费模块的线程数，数量20个
        t = threading.Thread(target=fun_2)
        threads.append(t)

    for t in threads:   #启动所有线程
        t.start()

    for t in threads:   #挂起所有线程
        t.join()

    print("work finished. Time：",time.ctime())

if __name__ == '__main__':
    main()
