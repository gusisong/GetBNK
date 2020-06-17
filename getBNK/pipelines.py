# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import shutil


class OriginBNKPipeline(object):
    def open_spider(self, spider):
        if spider.name == 'OriginBNK':
            if not os.path.exists('./cache_OriginBNK'):
                os.mkdir('./cache_OriginBNK')
            else:
                shutil.rmtree('./cache_OriginBNK')
                os.mkdir('./cache_OriginBNK')

        if spider.name == 'LatestBNK':
            if not os.path.exists('./cache_LatestBNK'):
                os.mkdir('./cache_LatestBNK')
            else:
                shutil.rmtree('./cache_LatestBNK')
                os.mkdir('./cache_LatestBNK')

    def process_item(self, item, spider):
        if spider.name == 'OriginBNK':
            # 清洗数据
            if item["零件号"] != None:
                item["零件号"] = item["零件号"].split('：')[1]

            if item["供应商SAP号"] != None:
                item["供应商SAP号"] = item["供应商SAP号"].split('：')[1]

            if item["采购工厂"] != None:
                item["采购工厂"] = item["采购工厂"].split('：')[1]

            if item["价格类型"] != None:
                item["价格类型"] = item["价格类型"].split('：')[1][-3:]

                # print(item)
        return item


class LatestBNKPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'LatestBNK':
            # 清洗数据
            if item["零件号"] != None:
                item["零件号"] = item["零件号"].split('：')[1]

            if item["供应商SAP号"] != None:
                item["供应商SAP号"] = item["供应商SAP号"].split('：')[1]

            if item["采购工厂"] != None:
                item["采购工厂"] = item["采购工厂"].split('：')[1]

            if item["价格类型"] != None:
                item["价格类型"] = item["价格类型"].split('：')[1][-3:]

                # print(item)
        return item
