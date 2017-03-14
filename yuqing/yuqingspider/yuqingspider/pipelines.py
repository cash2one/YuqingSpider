# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import redis
import urllib2
import MySQLdb
import random
from common.conn_mysql import conn_mysql
from common.conn_mongo import client_mongo
from common.md5 import md5


class YuqingspiderPipeline(object):

    def __init__(self):
        # mysql
        # self.conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='123', db='yuqing')
        self.conn = conn_mysql()
        self.mysqlop = self.conn.cursor()
        # redis
        self.r_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        # mongoDB
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
        try:

            url_md5 = md5(item['url'])
            # self.r_conn.set(url_md5, html_body.read())
            # item['html_body'] = None

            sqli = "insert into spider_content values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            news = {'content': item}

            if item['From'] == '0':
                # self.mysqlop.execute("insert into spider_content values('url_md5')")
                # self.mysqlop.execute(sqli, (url_md5, None, item['spider_name'], item['catch_date'],
                #                             item['From'], item['url'], item['title'].encode('utf-8'), item['summary'].encode('utf-8'), item['site_url'],
                #                             None, None, None, item['site_name'].encode('utf-8'), None))

                self.db.emergency.insert(news)
            elif item['From'] == '1' or item['From'] == '3':
                # self.mysqlop.execute(sqli, (url_md5, item['publish_time'], item['spider_name'], item['catch_date'],
                #                             item['From'], item['url'], item['title'].encode('utf-8'), item['summary'].encode('utf-8'), item['site_url'],
                #                             None, None, None, item['site_name'].encode('utf-8'), None))

                self.db.news.insert(news)
            elif item['From'] == '2':

                # self.mysqlop.execute(sqli, (url_md5, item['publish_time'], item['spider_name'], item['catch_date'],
                #                             item['From'], item['url'], item['title'].encode('utf-8'), item['summary'].encode('utf-8'), item['site_url'],
                #                             item['author'].encode('utf-8'), item['replay_times'], item['view_times'], item['site_name'].encode('utf-8'), None))
                self.db.bbs.insert(news)

        except Exception, e:
            print 'pipeline error', e

    def close_spider(self, spider):
        # commit task and close mysql
        self.mysqlop.close()
        self.conn.commit()
        self.conn.close()
        pass

if __name__ == "__main__":
    # print '\xe5\xa4\xa9\xe5\xa4\xa9'.encode('utf8')
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(a)
    for i in a:
        print i
