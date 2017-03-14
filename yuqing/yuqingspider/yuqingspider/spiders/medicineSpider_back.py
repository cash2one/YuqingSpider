# !/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'wtq'

import codecs
import json
import sys
import time
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from scrapy.utils.response import get_base_url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


reload(sys)
sys.setdefaultencoding('utf-8')


class ProductSpider(Spider):
    name = "medicineSpiderBack"

    allowed_domains = ["gov.cn"]

    start_urls = [
        "http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=124356560303886909015737447882",
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

        page_template = '//img[@src="images/dataanniu_07.gif"]'
        content_file = open("/home/wtq/medicine_out.txt", "wb")

        print 'in base url......', get_base_url(response)

        self.driver.get(response.url)  # 获取二级select
        # 以下为取下一页的内容，直到所有页被取完为止
        i = 0
        while True:
            i = i + 1
            print "get the ith page", i
            # 获取下一页的按钮点击
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, page_template)))

            p_url = self.driver.current_url
            print 'url............', p_url

            # extract object element
            blocks = self.driver.find_elements_by_xpath('//div[@id="content"]/table[2]/tbody/tr/td[@height="30"]')
            for block in blocks:
                print 'extract info @@@@@@@@@', block.text
                content_file.writelines(str(block.text) + "\n")

            try:
                pagedown = self.driver.find_element_by_xpath(page_template)

                # 首先判断按钮是否失效，失效即当前已是最后一页，直接退出
                if pagedown.get_attribute("onclick") == None:
                    break
                else:
                    pagedown.click()
                    time.sleep(3)
                    WebDriverWait(self.driver, 10)

            except Exception, e:
                print "on client button error", e
                content_file.close()
                self.driver.close()

            # self.get_item()
        content_file.close()
        self.driver.close()

    def close(self, spider):
        self.file.close()

