##	Scrapy爬虫数据入库

#### 	环境
-	python3.7
-	Scrapy==1.5.1
-	PyMySQL==0.9.3

####	启动命令
-	scrapy crawl goods_spider -a keyword=关键字 -a pagenum=爬取页数

####	程序流程
-	1.启动命令接受传递的2个参数到淘宝网爬取相应关键字商品数据完成爬取要求的页数->设计pipeline保存数据到MySql数据库
