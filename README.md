淘宝网商品信息爬取相关
--------------------

  1.文件taobao_spider.py是基础的爬虫，爬取速度2-3秒一个页面，受网速影响较大，商品解析时间占比较大。<br>
  2.时间：2017/3/21，文件taobao_spider.py，优化了正则匹配的模式，从贪婪匹配改成非贪婪匹配，解析速度快5-6倍。现在爬取一个页面只有0.5秒左右，受网速影响。
