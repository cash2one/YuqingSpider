#coding:utf-8
__author__ = 'wtq'
from scrapy.spiders import Spider
from scrapy import Request

from scrapy.selector import Selector

from ..common.emergency import SearchEngines
from ..common.emergency import SearchEngineResultSelectors
from ..util.ExtractContent import extract_content
from ..items.BaseItems import BaseItem
import yuqingspider.settings as conf
from jieba.analyse import extract_tags
import time


class emergencySpider(Spider):
    name = 'emergencySpider'
    start_urls = []
    allowed_domains = []

    def __init__(self,  *args, **kwargs):
        """
        # For every site in SearchEngines, only crawl the first page's emergency
        :param args:
        :param kwargs:
        :return:
        """
        super(emergencySpider, self).__init__(*args, **kwargs)
        for name, url in SearchEngines.items():    
            self.start_urls.append({'url': url, 'name': name, 'xpath': SearchEngineResultSelectors[name]})

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'name': url['name'], 'xpath': url['xpath']})
    
    def parse(self, response):
        selector = response.meta['xpath']
        print 'selector ', selector
        blocks = Selector(response).xpath(selector['block'])
        for block in blocks:             
            link = block.xpath(selector['link']).extract()
            title = block.xpath(selector['title']).extract()
            #time = block.xpath(selector['time']).extract()
            item = BaseItem()
            item['url'] = ''.join(link).strip()
            item['title'] = ''.join(title).strip().encode('utf-8')
            item['summary'] = ' '.join(extract_tags(item['title'], 3))
            #item['time'] = ''.join(time).strip().encode('utf-8')
            item['site_name'] = response.meta['name']
            item['catch_date'] = str(int(time.time()))
            item['spider_name'] = 'emergencySpider'
            item['From'] = '0'
            item['site_url'] = response.url
            # print item
            yield item

