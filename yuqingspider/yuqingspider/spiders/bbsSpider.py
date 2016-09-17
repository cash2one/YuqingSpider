__author__ = 'tanlong'
# -*- coding: UTF-8 -*-
import time as TIME
from scrapy.spiders import Spider
from scrapy import Request
from ..common.searResultPages import searResultPages
from ..common.searchName import SearchNameNew
from ..common.searchEngines import SearchEngineResultSelectors
from ..common.searchEngines import SearchEngines
from scrapy.selector import Selector
from ..items.BaseItems import BaseItem
from ..util.transtime import transtime
from ..util.BBSSearch import BBS_url_extract
from ..util.transreply import transreply
from ..util.extracttime import extracttime
from ..util.translink import translink


class bbsSpider(Spider):
    name = 'bbsSpider'
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None

    def __init__(self, keyword='石油', se='baidu', pages=3, *args, **kwargs):
        """
        pages is the number of which the page that you want to crawl
        then it will create different url by different pages keyword etc...
        :param keyword:
        :param se:
        :param pages:
        :param args:
        :param kwargs:
        :return:
        """
        super(bbsSpider, self).__init__(*args, **kwargs)
        # self.keyword = keyword.lower().encode('utf-8')
        self.keyword = keyword
        for k, v in SearchNameNew.items():
            engine, names = k, v
            print engine, names
            engineUrl = SearchEngines[engine]
            if 'mod=forum' in engineUrl:
                #url中带有mod=forum的是论坛搜索
                try:
                    # BBS_url_extract的作用是，将搜索的关键词转化url中的表达形式
                    res = BBS_url_extract(engineUrl.split('?')[0], keyword)
                    for p in range(1, int(pages) + 1):
                        # create different url by the different page
                        url = engineUrl.format(res['keyword'], p, res['searchid'])
                        print 'changed_bbs_url', url
                        self.start_urls.append(
                            {'url': url, 'name': names, 'selector': SearchEngineResultSelectors[engine]})
                except:
                    print 'url failed...'
            else:
                for p in range(1, int(pages) + 1):
                    url = engineUrl.format(self.keyword, p)
                    print 'changed_not_bbs_url', url
                    self.start_urls.append({'url': url, 'name': names, 'selector': SearchEngineResultSelectors[engine]})

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'name': url['name'], 'selector': url['selector']})

    def parse(self, response):

        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        item = BaseItem()
        # get the match every item's model
        self.selector = response.meta['selector']
        blocks = Selector(response).xpath(self.selector['block'])

        for block in blocks:
            link = block.xpath(self.selector['link']).extract()
            title = block.xpath(self.selector['title']).extract()
            source = block.xpath(self.selector['from']).extract()
            abstract = block.xpath(self.selector['abstract']).extract()
            author = block.xpath(self.selector['author']).extract()
            answerandlookup = block.xpath(self.selector['answerandlookup']).extract()

            # print answerandlookup
            try:
                link = translink(link, response.url)
            except Exception, e:
                print e

            if len(title) == 0:
                print 'title is null'
                return

            try:
                # ans->回复数 lookup->浏览数
                ans = '0'
                lookup = '0'
                if len(answerandlookup) != 0:
                    ans, lookup = transreply(answerandlookup[0])
                print ans, lookup
            except Exception, e:
                print e

            time = block.xpath(self.selector['time']).extract()[0]
            print time

            try:
                time = extracttime(time)
                print time
                time = transtime(time.strip())
                print time
            except Exception, e:
                print e
                print ''.join(source), ''.join(title), 'error'

            item['publish_time'] = str(time)
            item['cate_name'] = "bbssearch"
            item['catch_date'] = str(int(TIME.time()))
            item['From'] = "2"
            item['url'] = ''.join(link).strip()
            item['title'] = ''.join(title).strip()
            item['summary'] = ''.join(abstract).strip()
            item['site_url'] = response.url
            item['author'] = ''.join(author).strip()
            item['comments'] = ''.join(ans).strip()
            item['view'] = ''.join(lookup).strip()
            item['name'] = response.meta['name']
            if item['url']:
                yield item
