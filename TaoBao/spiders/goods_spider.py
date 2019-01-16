import scrapy 
from TaoBao.items import TaobaoItem
import time,hashlib
from scrapy.http import Request
from scrapy.selector import Selector
import urllib
import json
import re

class TaobaoSpider(scrapy.Spider):

	""" 爬取淘宝移动端商品数据存入MySQL""" 

	name = 'goods_spider'
	# allowed_domains = ["acs.m.taobao.com"]	
	tb_cookies = {"uc1":"cookie14=UoTYMb63bkLyoA%3D%3D&lng=zh_CN","t":"9e4af16f0edb4bcd2ba4c08fb1f0d539","csg":"88e86296","cna":"RfeKFDGyMH8CAcFwhT67Izg7","thw":"cn","skt":"fca4bcb533158ddd","l":"bBryAjPgvMrVwAjCBOCanurza77OSBRYYuPzaNbMi_5CO6Ts0__OlVhisF96V6CR_58B45FoCRp9-etUZ","uc3":"id2=&nk2=&lg2=","sn":"%E6%B7%B1%E5%9C%B3%E5%B8%82%E8%BE%89%E5%BD%A9%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%3A%E6%9B%8C%E8%B5%9F","_mw_us_time_":"1547187075929","v":"0","unb":"4161981099","_m_h5_tk":"592bf7291d6e6288cd6a9f00b254f43a_1547196798137","x":"2777370312","_m_h5_tk_enc":"69e70465943c3a16e817221e02967f6b","tracknick":"","isg":"BEJCObHEqiUbAbZ5j7cAFldCn0GkE0YtzRjMZoxbbrVg3-JZdKOWPciNiVWjlL7F","apushb6629951a76e6744507c9a12fe891b0e":"%7B%22ts%22%3A1547187080680%2C%22parentId%22%3A1547187077675%7D","_tb_token_":"51eeb365eb855","cookie2":"1dff156389806f616dc38346683011a0"}
	head = {
				'Accept': '*/*',
				'Accept-Encoding': 'gzip, deflate, br',
				'Accept-Language': 'zh-CN,zh;q=0.9',
				'Cache-Control': 'no-cache',
				'Connection': 'keep-alive',
				'Host': 'acs.m.taobao.com',
				'Pragma': 'no-cache',
				'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
	def start_requests(self):

		""" 爬取数据 """

		keyword= getattr(self, 'argdata', None) 
		pagenum= getattr(self, 'pagenum', None) 
		pagenum = int(pagenum)+1
		for page in range(1,pagenum):
			start_url = 'https://acs.m.taobao.com/h5/mtop.taobao.wsearch.h5search/1.0/'
			token = self.tb_cookies['_m_h5_tk'].split('_')[0]
			data = '{"q":"%s","search":"提交","tab":"all","sst":"1","n":20,"buying":"buyitnow","m":"api4h5","token4h5":"","abtest":"24","wlsort":"24","style":"list","closeModues":"nav,selecthot,onesearch","page":%s}' %(keyword,str(page))
			# 计算Sign
			t = int(time.time()*1000)
			src = token+'&'+str(t)+'&12574478&' + data
			m2 = hashlib.md5()
			m2.update(src.encode("utf8"))
			sign = m2.hexdigest()
			parame = {
				'jsv': '2.3.16',
				'appKey': '12574478',
				't': t,
				'sign': sign,
				'api': 'mtop.taobao.wsearch.h5search',
				'v': '1.0',
				'H5Request': 'true',
				'ecode': '1',
				'AntiCreep': 'true',
				'AntiFlool': 'true',
				'type': 'jsonp',
				'dataType': 'jsonp',
				'callback': 'mtopjsonp3',
				'data': data
						}
			start_url = start_url +'?'+ urllib.parse.urlencode(parame)
			yield Request(start_url ,method='GET', headers=self.head,cookies = self.tb_cookies,callback = self.parse)
	

	def parse(self,response):

		""" 处理数据 """
		
		str_json = response.body.decode(encoding='utf-8')
		resp_json = json.loads(re.match(".*?({.*}).*", str_json, re.S).group(1))
		
		page_data_list = resp_json['data']['listItem']
		for page_data in page_data_list:
			tb_item = TaobaoItem()
			tb_item['goods_url'] = page_data['url']
			tb_item['title'] = page_data['title']
			tb_item['pic_url'] = page_data['img2']
			tb_item['price'] = page_data['originalPrice']
			tb_item['sale'] = page_data['act']
			tb_item['addresss'] = page_data['location']
			yield tb_item


		