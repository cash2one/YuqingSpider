# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wtq'

import codecs
import json
import sys
import time
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from scrapy.utils.response import get_base_url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
# from etao.item import EtaoItem
from lib2to3.pgen2.tokenize import Ignore

reload(sys)
sys.setdefaultencoding('utf-8')


class ProductSpider(Spider):
    name = "medicineSpider"

    allowed_domains = ["gov.cn"]

    start_urls = [
        "http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=120&tableName=TABLE120&title=%CA%B3%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5%28SC%29&bcId=145275419693611287728573704379",
    ]

    def __init__(self):

        self.file = codecs.open("webdata" + time.strftime('%Y-%m-%d %X', time.localtime()).replace(':', '-') + ".json",
                                'w', encoding='utf-8')

        # in my laboratory use socks proxy to get internet
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.socks", "10.108.115.114")
        profile.set_preference("network.proxy.socks_port", 6176)
        profile.update_preferences()

        self.driver = webdriver.Firefox(firefox_profile=profile)

    def parse(self, response):

        print 'in base url......', get_base_url(response)
        response = response.replace(body=response.body.replace('<em>', '').replace('</em>', ''))
        blocks = Selector(response).xpath('//td[@height="30"]')

        for block in blocks:
            info = block.xpath(".//a/text()").extract()
            if len(info) > 0:
                print info[0]

        #self.driver.get(response.url)  # 获取二级select
        #self.driver.close()

    def close(self, spider):
        self.file.close()

    def get_item(self):

        WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='content']/table")))
        tables = self.driver.find_elements_by_xpath("//div[@id='content']/table")
        aaa = tables[1].find_elements_by_xpath("descendant::a")

        for a in aaa:
             # item = EtaoItem()
            item = {}
            item['name'] = a.text

            contents = a.get_attribute('href').split(",")

            item['url'] = "http://app1.sfda.gov.cn/datasearch/face3/" + contents[1]

            #             printa.text,contents[1]
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            print line
            self.file.write(line)


    # yield item

# if __name__ == '__main__':
#     settings = get_project_settings()
#
#     process = CrawlerProcess(settings)
#
#     process.crawl(ProductSpider)
#
#     process.start()
