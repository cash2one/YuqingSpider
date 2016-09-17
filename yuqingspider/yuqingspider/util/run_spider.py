# !/usr/bin/env python
# -*-coding: utf-8-*-
__author__ = 'wtq'

from ..spiders.bbsSpider import bbsSpider
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings


def spider_closing(spider):
    log.msg("Closing reactor", level=log.INFo)
    reactor.stop()


def spider_starting():
    log.start(loglevel=log.DEBUG)
    settings = Settings()

    # crawl responsibly
    settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
    crawler = Crawler(settings)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)

    crawler.configure()
    crawler.crawl(bbsSpiders(keyword="石油"))
    crawler.start()
    reactor.run()

if __name__ == "__main__":
    spider_starting()
