#coding=utf8
__author__ = 'tanlong'

from scrapy import Item, Field
from scrapy.contrib.loader import ItemLoader

class SearchItem(Item):
    spider_type = Field()
    publish_time = Field()
    site_source = Field()
    site_type = Field()
    site_url = Field()
    task_id = Field()
    title = Field()
    content = Field()
    author = Field()
    catch_date = Field()
