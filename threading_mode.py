#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Subject：多线程测试建模-生产者消费者模型
Note：用生产者模块代替request请求模块，处理速度一次0.3s-0.6s，用消费者模块代替正则解析模块，处理速度一次0.006s-0.007s。
      模拟总共请求1000个页面，用100个线程进行请求处理，1个线程进行解析处理，所需时间约9.2s(timeout:1s)
      模拟总共请求1000个页面，用100个线程进行请求处理，2个线程进行解析处理，所需时间约5.8s(timeout:1s)
      模拟总共请求1000个页面，用100个线程进行请求处理，3个线程进行解析处理，所需时间约5.8s(timeout:1s)
      模拟总共请求1000个页面，用100个线程进行请求处理，5个线程进行解析处理，所需时间约5.8s(timeout:1s)
      在消费线程增多的情况下，所需时间却没有降低，是因为只需要2个消费线程就能跑满，生产已经跟不上消费的速度，其他的消费线程都在等待。
Software: PyCharm
File: taobao_spider.py
Time：2018/3/23
Author：Pychenn
Version：V2.0
'''

import time
import threading
import queue
import random

#生产者模块，模拟请求处理函数
def fun_1():
    while 1:
        i = url_queue.get(1)        #从url队列里拿取数据，进行相应处理
        time.sleep(random.uniform(0.30,0.60))     #模拟处理操作
        html = random.randint(1,100)
        print("生产%s的数据：%s" % (i+1,html))
        html_queue.put(html)      #把生产好的数据放入html队列里
        print("生产后的队列size：%s"%html_queue.qsize())
        if url_queue.qsize() ==0:       #url队列为空，说明所有url请求完毕，生产线程关闭
            break

#消费者模块，模拟解析处理函数
def fun_2():
    while 1:
        try:
            data = html_queue.get(1,timeout=1)        #从html队列里拿取数据，进行相应处理
            time.sleep(random.uniform(0.006,0.007))     #模拟处理操作
            print("消费的数据：%s"%data)
            print("消费后的队列size：%s" % html_queue.qsize())
        except queue.Empty:
            break

#main()函数，程序执行流程
def main():
    global url_queue,html_queue
    url_queue = queue.Queue(1000)   #创建存放url的队列，设定最大值1000
    html_queue = queue.Queue(200)   #创建存放html的队列，设定最大值200
    threads = []    #存放所有线程的List
    print("Work started at time：",time.clock())
    for p in range(500):   #总共需要请求的页面数，创建url队列
        url_queue.put(p,1)

    for i in range(100):    #创建生产模块的线程，数量:100
        t = threading.Thread(target=fun_1)
        threads.append(t)

    for i in range(2):     #创建消费模块的线程，数量:2
        t = threading.Thread(target=fun_2)
        threads.append(t)

    for t in threads:   #启动所有线程
        t.start()

    for t in threads:   #挂起所有线程
        t.join()

    print("Work finished at time：",time.clock())

if __name__ == '__main__':
    main()
