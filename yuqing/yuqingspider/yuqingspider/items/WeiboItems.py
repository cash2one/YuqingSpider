#coding=utf8
__author__ = 'tanlong'

from seCrawler.items.BaseItems import BaseItem
from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Join

import seCrawler.util.FilterOper as fo

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class WeiboComItem(BaseItem):
    attitude = Field()
    comments = Field()
    repost = Field()
    user_url = Field()
    comments_text = Field()
#抓取数据清洗类

class WeiboComItemLoader(ItemLoader):
    default_item_class = WeiboComItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()

    content_in = MapCompose(fo.removeBlankStr, fo.filterHtml)

    comments_in = MapCompose(fo.getNum)

    repost_in =  MapCompose(fo.getNum)
