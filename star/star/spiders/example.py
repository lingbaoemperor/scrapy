# -*- coding: utf-8 -*-
import scrapy
from star.items import StarItem
import json

class ExampleSpider(scrapy.Spider):
    name = 'example'
    #allowed_domains = ['https://cn.bing.com/images'

    def __init__(self,category=None,*args,**kwargs):
        super(ExampleSpider,self).__init__(*args,**kwargs)
        pre = 'https://cn.bing.com/images/async?count=35&IG=A43F2EA031F3493CA70525942043CB73&iid=images.6102&lostate=r&mmasync=1&q={key_word}&relp=35&SFX=1&first={page_num}'
        star_name = ['vehicle','车']
#        star_name = ['vehicle']
        star_count = len(star_name)
        #每种动物需要多少张，每页35张,这里指定页数加1
        sheets = 2
		#n个关键字
        for i in range(star_count):
            first = 1
            for j in range(35,sheets*35,35):
                #一页35张，first参数展示不知道怎么回事,指定40递增 ,会重复下载一部分
                self.start_urls.append(pre.format(key_word=star_name[i],page_num=first))
                first += 40
#            print(self.start_urls[0])
        
    #需要登陆的网站提交一次登陆信息，还可指定回掉函数，此处用不上
#    def start_requests(self):
#        yield scrapy.FormRequest('http://image.baidu.com/',formdata={},callback=self.parse)
    
    def parse(self, response):
        #self.logger.info('Hi,this is an item page! %s',response.url)
        item = StarItem()
        sel = scrapy.selector.Selector(response)
        #这个是小图，不要
        #img_urls = sel.xpath('/html/body/div[@class="dg_b"]/div[@class="dgControl hover"]/ul/li/div[@class="iuscp varh"]/div[@class="imgpt"]/a[@class="iusc"]/div[@class="img_cont hoff"]/img[@class="mimg"]/@src').extract()
        #这个是大图
        img_urls = sel.xpath('/html/body/div[@class="dg_b"]/div[@class="dgControl hover"]/ul/li/div[@class="iuscp varh"]/div[@class="imgpt"]/a[@class="iusc"]/@m').extract()
#        print(len(img_urls))
#        print(img_urls)
#        with open('a.txt','wb') as f:
#            f.write(response.body)
        #图片下载链接
        for tip in img_urls:
            try:
                url = json.loads(tip)['murl']
                item['addr'] = url
                yield item
            finally:
                print(tip)