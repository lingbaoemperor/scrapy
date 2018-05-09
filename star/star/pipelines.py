# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib
from scrapy.exceptions import DropItem
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class StarPipeline(object):
    def process_item(self, item, spider):
        print(item)
        addr = item['addr']
        res = urllib.urlopen(addr)
        if str(res.status) != '200':
            print('失败!')
            return
##        name = str(item['name'])
        path = './img/'+item['name']
        if os.path.exists(path) == False:
            os.makedirs(path)
        number = str(len(os.listdir(path)))+'.jpg'
        with open(path+number,'wb') as f:
            f.write(res.read)
        print('ok!')
        return item
        
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item