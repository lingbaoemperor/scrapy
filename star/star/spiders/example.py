# -*- coding: utf-8 -*-
import scrapy
from star.items import StarItem
import json

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['image.baidu.com/search']

    def __init__(self,category=None,*args,**kwargs):
        super(ExampleSpider,self).__init__(*args,**kwargs)
        pre = 'https://image.baidu.com/search/acjson?\
                tn=resultjson_com&ipn=rj&ct=201326592&\
                is=&fp=result&queryWord+=&cl=2&lm=-1&\
                ie=utf-8&oe=utf-8&adpicid=&st=-1&\
                z=&ic=0&s=&se=&tab=&width=&height=&\
                face=0&istype=2&qc=&nc=1&\
                fr=&\
                rn=30&gsm=1e&\
                word='
        star_name = ['吴京','阿曼达·塞弗里德']
        temp_urls = [pre + star_name[i] for i in range(len(star_name))]
        star_count = len(star_name)
        #需要多少张，每页30张
        sheets = 21*30
        for i in range(star_count):
            for j in range(30,sheets,30):
                self.start_urls.append(temp_urls[i]+'&pn=%d' % j)
        print(self.start_urls)
        
    #需要登陆的网站提交一次登陆信息，还可指定回掉函数，此处用不上
#    def start_requests(self):
#        yield scrapy.FormRequest('http://image.baidu.com/',formdata={},callback=self.parse)
    
    def parse(self, response):
        self.logger.info('Hi,this is an item page! %s',response.url)
        item = StarItem()
        with open('a.txt','wb') as f:
            f.write(response.body)
        dic= json.loads(response.body)
        #人名和图片下载链接
        item['name'] = dic['queryExt']
        dic = dic['data']
        for addr in dic:
            if 'thumbURL' in addr.keys():
                item['addr'] = addr['thumbURL']
                yield item