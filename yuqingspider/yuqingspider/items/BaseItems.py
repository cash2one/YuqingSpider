#coding=utf8
__author__ = 'tanlong'

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
    comments = Field()
    view = Field()
    url = Field()
    name = Field()
    author = Field()
    page = Field()
    cate_name = Field()
    From = Field()
    depth = Field()
