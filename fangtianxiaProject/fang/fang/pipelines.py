# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class FangPipeline(object):
    def __init__(self):
        self.fp = open('fang.json','w',encoding='utf-8')

    def process_item(self, item, spider):
        obj = dict(item)
        str = json.dumps(obj,ensure_ascii=False)
        self.fp.write(str+"\n")
        return item

    def close_spider(self,spider):
        self.fp.close()
