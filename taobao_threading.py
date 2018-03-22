#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Subject：淘宝网爬虫-多线程版
Note:1.由于存储函数storage()里用到全局变量，所以要在本文件内重写一次，为了方便，去除了控制页码的变量i。
     2.由于爬取一个页面的时间主要花费在request请求上（请求时间0.5s，解析时间0.006s，存储时间0.003s），所以需要用多线程
     进行request请求，一个线程进行解析存储即可。
     3.由于解析存储的速度太快，请求函数产生html的速度远远跟不上，所以更改模型架构，先让请求线程都处理完，
     把返回的html依次放入队列里，再进行解析存储。
     4.由于存储的数据是放在excel中的，由k确定行下标，为了防止写入数据冲突，存储函数不能用多线程。
     5.由于存放在队列中的html是随机页面的，所以解析函数拿到的html也是随机页面的，为了保证所有数据都被成功写入，
     所以原来的捕捉错误退出页面的策略不能用，改为请求数最大为113页。
Software: PyCharm
File: taobao_threading.py
Time：2018/3/22
Author：Pychenn
Version：V2.0
'''

import time
import threading
import queue
import xlwt
from taobao_spider import *

#存储管理，将信息写入Excel表格
def storage(ws,infos):
    global k    #全局变量，定位excel的行下标，每写入一行数据，数值加1
    for info in infos:
        ws.write(k,0,info.get("raw_title"))
        ws.write(k, 1, info.get("detail_url"))
        ws.write(k, 2, info.get("nick"))
        ws.write(k, 3, info.get("view_price"))
        ws.write(k, 4, info.get("item_loc"))
        ws.write(k, 5, info.get("view_sales"))
        ws.write(k, 6, info.get("view_fee"))
        k = k+1
    print("商品信息写入完成")
    return

#请求函数模块
def fun_1(name):
    while 1:
        i = url_queue.get(1)        #从url队列里拿取数据，进行相应处理
        html = search_fun(name,i)
        html_queue.put(html,1)      #把生产好的数据放入html队列里
        print("生产后的队列size：%s"%html_queue.qsize())
        if url_queue.qsize() == 0:       #url队列为空，说明所有url请求完毕，线程关闭
            break

#解析存储函数模块
def fun_2(ws):
    #time.sleep(0.5) #先等待生产
    while 1:
        html = html_queue.get(1)        #从html队列里拿取数据，进行相应处理
        data = shangping(html)          #解析
        storage(ws, data)               #存储
        print("消费后的队列size：%s" % html_queue.qsize())
        if html_queue.qsize() ==0:      #html队列为空，说明所有生产好的html都处理完毕，线程关闭
            break


#main()函数，程序执行流程
def main():
    global url_queue
    url_queue = queue.Queue(1000)   #创建存放url的队列，最大值1000
    global html_queue
    html_queue = queue.Queue(200)   #创建存放html的队列，最大值200
    threads = []    #存放所有线程的队列

    name = input("请输入搜索的商品名称（如：男装）：")
    #在main()函数中建立excel，把对象ws传入每次调用的存储函数
    wb = xlwt.Workbook("encoding=utf-8")
    ws = wb.add_sheet(name)
    format(ws)
    global k    #全局变量k，定位excel的行下标，每写入一行数据，数值加1
    k = 1

    # 先写首页异步加载的数据
    infos = first_page(name)
    storage(ws, infos)
    # 再写剩下正常加载的数据
    for p in range(110):   #总共需要请求的页面数，创建url队列
        url_queue.put(p,1)

    for i in range(100):    #创建生产模块的线程，数量:100
        t = threading.Thread(target=fun_1,args=(name,))
        threads.append(t)

    for t in threads:   #启动所有线程
        t.start()

    for t in threads:   #挂起所有线程
        t.join()
    print("product over. Time：", time.clock())

    fun_2(ws)
    print("consume over. Time：",time.clock())

    # 命名保存
    print("商品信息获取存储完毕，程序结束运行")
    wb.save("%s.xls" % name)

if __name__ == '__main__':
    main()
