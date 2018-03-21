#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Subject：可搜索的淘宝网商品信息采集器
Note：   基于参数q,s实现检索和翻页，每页s的值增加44.爬取的信息写入对应名字的Excel文档中.
Software: PyCharm
File: taobao_spider.py
Time：2018/3/21
Author：Pychenn
Version：V1.1
'''

import requests
import re
import json
import xlwt
import time

#商品搜索函数，返回搜索结果的html
def search_fun(name,i):
    url = "https://s.taobao.com/search?"    #检索基础地址
    params = {
        "q":name,   #关键字q控制搜索的商品名字
        "s":i*44    #关键字s控制搜索的页面，每页依次增加44
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWeb \
        Kit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"   #爬虫也是有尊严的，拒绝裸奔
    }
    response = requests.get(url,params = params,headers = headers)
    if response.status_code == 200:
        #对得到页面进行判断，防止返回空的html
        if response.text != "":
            response.encoding = "utf-8"
            print("第%s页 网页请求成功" % (i + 1))
            return response.text    #返回html
        else:
            print("第%s页 请求到空页面，尝试再次请求"%(i+1))
            return search_fun(name,i)
    else:
        print("第%s页 网页请求失败，尝试再次请求" %(i+1))
        return search_fun(name,i)

#商品信息解析函数，返回需要的商品信息
def jiexi(html):
    infos = []  #商品信息存储队列
    fi = re.findall(r"g_page_config = ({.*?});.*?g_srp_loadCss",html,re.S)  #用非贪婪匹配，解析速度比贪婪匹配快几倍
    if fi !=[]:
        #将json数据转成dic方便处理
        data = json.loads(fi[0])
        data_lists = data["mods"]["itemlist"]["data"]["auctions"]   #每页搜索到的商品信息存放处，每次44个（首页36个）
        #分别获得每个商品信息
        for data_list in data_lists:
            info = {
                "raw_title": data_list.get("raw_title"),  # 商品名字
                "detail_url": data_list.get("detail_url"),  # 商品链接
                "nick": data_list.get("nick"),  # 店铺名字
                "view_price": data_list.get("view_price"),  # 商品价格
                "item_loc": data_list.get("item_loc"),  # 店铺地址
                "view_sales": data_list.get("view_sales"),  # 付款人数
                "view_fee": data_list.get("view_fee")  # 邮费
            }
            infos.append(info)  #每次成功解析后将数据添加到list中
        print("商品信息解析成功")
    return infos

#首页异步加载的12条信息，单独处理
def first_page(name):
    infos = []  #商品信息存储队列
    # 异步加载的地址基于参数m,q实现。q是搜索的商品名，m是固定字符customized
    url2 = "https://s.taobao.com/api?"
    params = {
        "q": name,
        "m":"customized"
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWeb \
        Kit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"   #遨游浏览器的user-agent
    }
    response = requests.get(url2, params=params, headers=headers)
    if response.status_code == 200:
        print("第1页 异步加载请求成功")
        response.encoding = "utf-8"
        # 将html转成json数据方便处理
        data = json.loads(response.text)
        data_lists = data["API.CustomizedApi"]["itemlist"]["auctions"]  # 首页的商品信息存放处，12个
        # 分别获得每个商品信息
        for data_list in data_lists:
            info = {
                "raw_title": data_list.get("raw_title"),  # 商品名字
                "detail_url": data_list.get("detail_url"),  # 商品链接
                "nick": data_list.get("nick"),  # 店铺名字
                "view_price": data_list.get("view_price"),  # 商品价格
                "item_loc": data_list.get("item_loc"),  # 店铺地址
                "view_sales": data_list.get("view_sales"),  # 付款人数
                "view_fee": data_list.get("view_fee")  # 邮费
            }
            infos.append(info)
        return infos
    else:
        print("第1页 异步加载错误，尝试再次请求")
        return first_page(name)

#定义excel信息存储每列对应的内容
def format(ws):
    ws.write(0,0,"商品名字")
    ws.write(0,1,"商品链接")
    ws.write(0, 2, "店铺名字")
    ws.write(0, 3, "商品价格")
    ws.write(0, 4, "店铺地址")
    ws.write(0, 5, "付款人数")
    ws.write(0, 6, "邮费")
    return

#存储管理，将信息写入Excel表格
def storage(ws,infos,i=0):
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
    print("第%d页 信息写入完成" % (i + 1))
    print("Time：%s"%time.ctime())
    return

#main()函数，程序执行流程
def main():
    name = input("请输入搜索的商品名称（如：男装）：")
    #在main()函数中建立excel，把对象ws传入每次调用的存储函数
    wb = xlwt.Workbook("encoding=utf-8")
    ws = wb.add_sheet(name)
    format(ws)
    global k    #全局变量k，定位excel的行下标，每写入一行数据，数值加1
    k = 1
    # 捕捉异常
    try:
        #先写首页异步加载的数据
        infos = first_page(name)
        storage(ws,infos)
        #再写正常加载的数据
        for i in range(0,150):   #翻页的页数控制,一般到114页就会提示未找到相关宝贝
            while 1:
                html = search_fun(name, i)
                data = jiexi(html)
                if data != []:
                    storage(ws,data,i)
                    break
                else:
                    print("第%d页 信息获取错误，尝试再次请求" % (i+1))
        # 命名保存
        print("商品信息获取存储完毕，程序结束运行")
        wb.save("%s.xls"%name)
    except KeyError:    #当页面提示未找到相关宝贝，正则解析的时候，会抛出KeyError异常
        print("由于获取不到更多数据，程序结束运行")
        wb.save("%s.xls" % name)

if __name__ == '__main__':
    main()
