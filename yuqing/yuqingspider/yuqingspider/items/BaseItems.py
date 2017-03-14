#coding=utf8
__author__ = 'tanlong'

import urllib2
from scrapy import Item, Field
from scrapy.contrib.loader import ItemLoader


class BaseItem(Item):
    spider_type = Field()
    publish_time = Field()
    site_source = Field()
    site_type = Field()
    site_url = Field()
    task_id = Field()
    title = Field()
    summary = Field()
    author = Field()
    catch_date = Field()
    comments_text = Field()
    replay_times = Field()
    view_times = Field()
    url = Field()
    site_name = Field()
    author = Field()
    page = Field()
    spider_name = Field()
    From = Field()
    depth = Field()
    html_body = Field()

if __name__ == '__main__':
    content = urllib2.urlopen('http://www.byr.edu.cn/')
    print content.read()
    print content.info()
