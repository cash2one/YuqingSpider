#!/usr/local/bin/python2.7
# coding:utf-8

import sys
import requests
import json

HOST_URL = 'http://localhost:6800'


def weibo(gearman_worker, job):

    param = json.loads(job.data)
    keyword = param['keyword']
    pages = param['pages']
    se = param['se']
    # curl http://localhost:6800/schedule.json -d project=default -d spider=weiboSpider -d se=weibohot

    res = requests.post(HOST_URL + '/schedule.json',
                        data={'project': 'default', 'spider': 'weiboSpider', 'se': se, 'pages': pages,
                              'keyword': keyword})

    return str("Job added")


def news():

    res = requests.post(HOST_URL + '/schedule.json',
                        data={'project': 'default', 'spider': 'newsSpider'})

    return str("Job added")


def bbs():

    res = requests.post(HOST_URL + '/schedule.json',
                        data={'project': 'default', 'spider': 'bbsSpider'})

    return str("Job added")


def blog():

    res = requests.post(HOST_URL + '/schedule.json',
                        data={'project': 'default', 'spider': 'blogSpider'})

    return str("Job added")


def deleteproject(parameter):
    url = HOST_URL + '/delproject.json'
    #print url
    data = {'project': parameter}
    res = requests.post(url, data=data)
    print res.text


def main():
    # 获取命令行传的参数
    if sys.argv[1] == 'news':
        news()
    elif sys.argv[1] == 'bbs':
        bbs()
    elif sys.argv[1] == 'blog':
        blog()
    elif sys.argv[1] == 'weibo':
        weibo()
    else:
        permater = sys.argv[1]
        deleteproject(permater)
if __name__ == "__main__":
    # main()
    # blog()
    # bbs()
    news()
