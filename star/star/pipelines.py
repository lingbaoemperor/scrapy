# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import urllib

class StarPipeline(object):
    def process_item(self, item, spider):
        #取出图片链接，下载图片
        addr = item['addr']
        res = urllib.request.urlopen(addr)
        if str(res.status) != '200':
            print('失败!')
            return
#       img/img_key/img_name.jpg
#       所有的图片放在一起了，现在只需要车的图片
        path = './img/'+'vehicle/'
        if os.path.exists(path) == False:
            os.makedirs(path)
        count = str(len(os.listdir(path)))
        name = count+'.jpg'
        with open(path+name,'wb') as f:
            f.write(res.read())
        print('ok!'+count)
        return item