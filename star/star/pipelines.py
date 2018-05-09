# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib

class StarPipeline(object):
    def process_item(self, item, spider):
        addr = item['addr']
        res = urllib.request.urlopen(addr)
        if str(res.status) != '200':
            print('失败!')
            return
##        name = str(item['name'])
        path = './img/'+str(item['name'])+'/'
        if os.path.exists(path) == False:
            os.makedirs(path)
        number = str(len(os.listdir(path)))+'.jpg'
        with open(path+number,'wb') as f:
            f.write(res.read())
        print('ok!')
        return item