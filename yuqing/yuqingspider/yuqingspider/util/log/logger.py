# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import os
import logging
from yuqingspider.yuqingspider.util.transtime import transtime
current_path = os.path.dirname(__file__)


def logings():
    logging.basicConfig(filename=current_path + '/logger.log', level=logging.INFO)
    log = logging
    return log

if __name__ == '__main__':
    a = '腾讯财经  2016年09月29日 15:00'
    string = ''.join(a).replace("\xc2\xa0", " ").split(' ', 1)
    print string[0].strip()
    print transtime(string[1].strip())

