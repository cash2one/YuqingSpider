# !usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import hashlib
__author__ = 'wtq'


def md5(str):
    """
    change any string to a md5 value
    :param str:
    :return:
    """
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

if __name__ == "__main__":
    body = urllib2.urlopen("http://gold.hexun.com/2016-09-18/186068918.html")
    print md5(body.read())
    print md5('http://forex.hexun.com/2016-09-20/186093271.html')
