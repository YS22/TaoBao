# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import connect

class TaobaoPipeline(object):
    def __init__(self):
        self.con = connect(host='193.112.133.62', user='scrapy_test', password='123456', db='scrapy_test', charset='utf8')
        self.obj = self.con.cursor()  # 游标对象

    def process_item(self, item, spider):
        sql = """ insert into tb_goods_info(goods_url,title,pic_url,price,sale,addresss) values ('%s','%s','%s','%s','%s','%s') """ %(item['goods_url'],item['title'],item['pic_url'],item['price'],item['sale'],item['addresss'])
        self.obj.execute(sql)
        self.con.commit()