# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wtq'

from yuqingspider.yuqingspider.spiders.newsSpider import newsSpider
from yuqingspider.yuqingspider.spiders.bbsSpider import bbsSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


#导入spider的settings 从而能够使用pipelines
process = CrawlerProcess(get_project_settings())
# process.crawl('bbsSpider')
# process.crawl('newsSpider')
news = newsSpider(se='baidu')
# process.crawl(news)
# process.start()

# 执行完爬虫命令后 再由
# subprocess.open(scrapy crawl newsSpider)
