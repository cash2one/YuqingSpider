# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from common.conn_mongo import client_mongo


class YuqingspiderPipeline(object):

    def __init__(self):
        client = client_mongo()
        self.db = client.spider

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        """
        deal the item which get from TencentSpider.parse_item
        :param item:
        :param spider:
        :return:
        """
        # for word in keywords:
        #     if word in item['content'] or word in item['title']:
        #         news = {"tencent_news": item}
        #         self.db.tencent_news.insert(news)
        #         break

        news = {"bbs_news": item}
        self.db.bbs_news.insert(news)

    def close_spider(self, spider):
        pass

