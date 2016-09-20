# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wtq'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import redis
from scrapy import Request
from scrapy.spiders import Spider
from ..common.md5 import md5
from ..common.searResultPages import searResultPages
from ..common.searchEngines import SearchEngineResultSelectors
from scrapy.selector import Selector
from ..items.BaseItems import BaseItem
from ..util.transtime import transtime


r = redis.StrictRedis(host='localhost', port=6379, db=0)


class newsSpider(Spider):
    name = 'newsSpider'
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None

    def __init__(self, keyword='石油', se='baidu', pages=1, *args, **kwargs):
        # 搜素关键词从redis中读取， 要使用的搜索引擎生成类的时候传入默认为youdao
        super(newsSpider, self).__init__(*args, **kwargs)
        self.item = BaseItem()

        # get keyword and se from redis
        keywords = r.lrange('news_keyword', 0, 6)
        ses = r.lrange('news_site', 0, 6)
        for se in ses:
            # for se in ses:
            for keyword in keywords:
                self.keyword = keyword.lower()
                self.searchEngine = se.lower()
                self.selector = SearchEngineResultSelectors[self.searchEngine]
                # 根据关键词与站点的名字与pages生成对应的不同的url
                pageUrls = searResultPages(keyword, se, int(pages))

                # 不同页面的url存储到start_urls中,start_urls中的每个url都会调用parse函数执行
                for url in pageUrls:
                    print(url)
                    self.start_urls.append({'url': url, 'selector': self.selector})

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'selector': url['selector']})

    def parse(self, response):

        self.selector = response.meta['selector']
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        blocks = Selector(response).xpath(self.selector['block'])

        for block in blocks:
            link = block.xpath(self.selector['link']).extract()
            title = block.xpath(self.selector['title']).extract()
            source = block.xpath(self.selector['from']).extract()
            print 'source ', source
            abstract = block.xpath(self.selector['abstract']).extract()

            if self.selector.has_key('time'):
                ctime = block.xpath(self.selector['time']).extract()[0]
                name = ''.join(source).strip()
            else:
                try:
                    print 'has no time'
                    string = ''.join(source).replace("\xc2\xa0", " ").split(' ', 1)
                    if len(string) >= 2:
                        ctime = transtime(string[1].strip())
                        name = string[0].strip()
                except Exception, e:
                    print 'extract time error', e
                    # print ''.join(source), ''.join(title), 'error'

            self.item['publish_time'] = str(ctime)
            self.item['From'] = "1"
            self.item['spider_name'] = "newsSpider"
            self.item['catch_date'] = str(int(time.time()))
            self.item['site_name'] = name
            self.item['url'] = ''.join(link).strip()
            self.item['title'] = ''.join(title).strip()
            self.item['summary'] = ''.join(abstract).strip()
            self.item['site_url'] = response.url

            if self.item['url']:
                yield self.item
                yield Request(self.item['url'], callback=self.parse_body)

                # yield self.item

    def parse_body(self, response):
        """
        url_md5 as key, html body as value then save to redis
        :param response:
        :return:
        """
        url_md5 = md5(response.url)
        html_body = response.body
        r.set(url_md5, html_body)
