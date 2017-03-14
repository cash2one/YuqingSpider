# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wtq'
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
import json
import chardet
import logging
import time
import time as TIME
from scrapy.spiders import Spider
from scrapy import Request
from ..common.config import CRAWLER_TIME_SIGN
from ..common.config import SIGN_TIME_STAMP
from ..common.conn_mysql import conn_mysql
from scrapy.selector import Selector
from datetime import datetime
from ..util.transtime import transtime
from ..util.BBSSearch import BBS_url_extract
from ..util.transreply import transreply
from ..util.extracttime import extracttime
from ..util.translink import translink
from ..util.redis_queue import RedisQueue

content_queue = RedisQueue("items")
mysql_conn = conn_mysql()

mysqlop = mysql_conn.cursor()
mysqlop.execute("SET NAMES utf8")
mysqlop.execute("SET CHARACTER_SET_CLIENT=utf8")
mysqlop.execute("SET CHARACTER_SET_RESULTS=utf8")
mysql_conn.commit()

#current_path = os.path.dirname(__file__)
#logging.basicConfig(filename=current_path + '/logger.log', level=logging.INFO)

content_dict = {}
mysqlop.execute("select cn_name, contentpage_template from t_source_used where type='bbs' and contentpage_template is not null")
conts = mysqlop.fetchmany(size=10000000)
for con in conts:
    content_dict[con[0]] = con[1]


class bbsSpider(Spider):
    name = 'bbsSpider'
    start_urls = []
    keyword = None
    searchEngine = None
    selector = None

    def __init__(self, se='baidu', pages=1, *args, **kwargs):
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
        # 查询的关键词由redis中的键值对， key: news_spider, value: list[keyword1, keyword2..]
        # self.item = dict()
        self.latest_time = dict()

        # get latest time from mysql
        mysqlop.execute("select source_name, latest_time, key_word from source_latest_time")
        times = mysqlop.fetchmany(size=10000000)
        for time_item in times:
            if time_item[0] not in self.latest_time:
                self.latest_time[time_item[0]] = dict()
            self.latest_time[time_item[0]][time_item[2]] = int(time.mktime(time_item[1].timetuple()))

        # get key word from mysql
        mysqlop.execute("select keyword from key_words")
        keywords = mysqlop.fetchmany(size=10000000)

        # get site template from mysql
        mysqlop.execute("select en_name, cn_name, url, template from t_source_used where type='bbs'")
        ses = mysqlop.fetchmany(size=10000000)

        for item in keywords:
            key_word = item[0]
            for se in ses:
                # for k, v in SearchNames.items():
                try:
                    source_name = se[1]
                    source_url = se[2]
                    selector = json.loads(se[3])
                except Exception, e:
                    logging.info('source parse error')
                url = None
                model_sign = 0
                res = ""
                # source time and key word not in table, then put it latest time in one month before
                insert_sql = "insert into source_latest_time(latest_time, source_name, key_word) values(%s, %s, %s)"
                initialize_crawl_time = datetime.strptime(CRAWLER_TIME_SIGN, '%Y-%m-%d %H:%M:%S')
                if source_name not in self.latest_time.keys():
                    self.latest_time[source_name] = dict()
                    self.latest_time[source_name][key_word] = SIGN_TIME_STAMP
                    mysqlop.execute(insert_sql, (initialize_crawl_time, source_name, key_word))
                    mysql_conn.commit()
                elif key_word not in self.latest_time[source_name].keys():
                    self.latest_time[source_name][key_word] = SIGN_TIME_STAMP
                    mysqlop.execute(insert_sql, (initialize_crawl_time, source_name, key_word))
                    mysql_conn.commit()

                if 'mod=forum' in source_url:
                    # url中带有mod=forum的是论坛搜索
                    model_sign = 1
                    try:
                        # BBS_url_extract的作用是，将搜索的关键词转化url中的表达形式
                        res = BBS_url_extract(source_url.split('?')[0], key_word)
                        url = source_url.format(res['keyword'], 1, res['searchid'])
                        print 'changed_bbs_url', url

                    except:
                        print 'url failed...'
                else:
                    model_sign = 0
                    # for p in range(1, int(pages) + 1):
                    url = source_url.format(key_word, 1)
                    print 'changed_not_bbs_url', url

                if url:
                    self.start_urls.append(
                            {'url': url, 'source_name': source_name, 'selector': selector, 'key_word': key_word,
                             'next_page': 2, 'source_url': source_url, 'model_sign': model_sign, 'res': res})

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url['url'], meta={'source_name': url['source_name'], 'selector': url['selector'],
                                            'key_word': url['key_word'], 'next_page': url['next_page'],
                                            'source_url': url['source_url'], 'model_sign': url['model_sign'], 'res': url['res']})

    def parse(self, response):

        mysqlop = mysql_conn.cursor()
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        item = dict()
        # get the match every item's model
        key_word = response.meta['key_word']
        source_name = response.meta['source_name']
        self.selector = response.meta['selector']
        source_url = response.meta['source_url']
        next_page = response.meta['next_page']
        model_sign = response.meta['model_sign']
        res = response.meta['res']
        over_time_sign = 1
        first_item_sign = 1

        # parse item by item
        blocks = Selector(response).xpath(self.selector['block'])
        for block in blocks:
            link = block.xpath(self.selector['link']).extract()
            title_raw = block.xpath(self.selector['title'])
            try:
                title = title_raw.xpath('string(.)').extract()[0]
            except Exception, e:
                title = ""

            source = block.xpath(self.selector['from']).extract()
            abstract_raw = block.xpath(self.selector['abstract'])
            try:
                abstract = abstract_raw.xpath('string(.)').extract()[0]
            except Exception, e:
                abstract = ""

            author = block.xpath(self.selector['author']).extract()
            answerandlookup = block.xpath(self.selector['answerandlookup']).extract()

            # print answerandlookup
            try:
                link = translink(link, response.url)
            except Exception, e:
                print e

            try:
                # ans->回复数 lookup->浏览数
                ans = '0'
                lookup = '0'
                if len(answerandlookup) != 0:
                    ans, lookup = transreply(answerandlookup[0])

            except Exception, e:
                print e

            try:
                ctime = block.xpath(self.selector['time']).extract()[0]
            except Exception, e:
                ctime = None

            try:
                if ctime!=None:
                    ctime = extracttime(ctime)
                    ctime = transtime(ctime.strip())

            except Exception, e:
                print e
                ctime = None

            if ctime == None:
                # publish time 解析为空则设置为当前时间的unix时间戳
                ctime = int(time.time())

            if ctime > self.latest_time[source_name][key_word]:
                if next_page == 2 and first_item_sign == 1:
                    update_sql = "update source_latest_time set latest_time=%s where source_name=%s and key_word=%s"
                    new_latest_time = datetime.fromtimestamp(ctime)
                    mysqlop.execute(update_sql, (new_latest_time, source_name, key_word))
                    mysql_conn.commit()
                    first_item_sign = 0

                item['publish_time'] = int(ctime)
                item['catch_date'] = str(int(TIME.time()))
                item['From'] = "bbs"
                item['url'] = ''.join(link).strip()
                item['title'] = ''.join(title).strip()
                item['summary'] = ''.join(abstract).strip()
                item['site_url'] = response.url
                item['author'] = ''.join(author).strip()
                item['replay_times'] = ''.join(ans).strip()
                item['view_times'] = ''.join(lookup).strip()
                item['site_name'] = source_name
                item['source_name'] = source_name
                item['key_word'] = key_word

                if item['url']:
                    item_json = json.dumps(item)
                    yield Request(item['url'], meta={'item': item_json}, callback=self.parse_body)
            else:
                over_time_sign = 0
                break
        # 本页解析完成生下一页的url
        if over_time_sign and next_page < 100 and blocks and len(blocks) > 5:
            if model_sign:
                # res = BBS_url_extract(source_url.split('?')[0], key_word)
                next_page_url = source_url.format(res['keyword'], next_page, res['searchid'])
            else:
                next_page_url = source_url.format(key_word, next_page)
            print 'request next page', next_page_url
            yield Request(next_page_url, meta={'selector': self.selector, 'source_name': source_name,
                                            'key_word': key_word, 'next_page': next_page + 1,
                                            'source_url': source_url, 'model_sign': model_sign, 'res': res})

    def parse_body(self, response):

        item = response.meta['item']
        body = response.body
        item = json.loads(item)

        if not isinstance(body, unicode):
            code_type = chardet.detect(body)['encoding']
            if code_type == 'GB2312':
                code_type = 'gbk'
            html_body = body.decode(code_type).encode('utf-8')
        else:
            html_body = body.encode('utf-8')

        if item['source_name'] in content_dict:
            item['text'] = response.xpath(content_dict[item['source_name']]).extract()

        item["html_body"] = html_body
        url_content = json.dumps(item)
        # print 'body', body
        if len(body) > 5:
            content_queue.put(url_content)
        else:
            logging.info(response.url)
