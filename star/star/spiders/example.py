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
                word=吴京&z=&ic=0&s=&se=&tab=&width=&height=&\
                face=0&istype=2&qc=&nc=1&\
                fr=&\
                pn=30&\
                rn=30&gsm=1e'
        star_name = ['吴京']
        self.start_urls = [pre + star_name[i] for i in range(len(star_name))]
#        print(self.start_urls)
        
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
        item['image_paths'] = [dic['queryExt']]
        dic = dic['data']
        for addr in dic:
            if 'thumbURL' in addr.keys():
                item['image_urls'] = [addr['thumbURL']]
                yield item