#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time


def transtime(time_str):
    time_str = time_str.strip()
    try:
        r = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M')) 
        return int(r)
    except Exception, e:
        try:
            r = time.mktime(time.strptime(time_str, '%Y年%m月%d日')) 
            return int(r)
        except Exception, e:
            try:
                r = time.mktime(time.strptime(time_str, '%Y-%m-%d'))
                return int(r)
            except Exception,e:
                if '分钟前' in time_str:
                    r = time.time() - int(time_str[0:time_str.index('分钟前')]) * 60
                    return int(r)
                elif '天前' in time_str:
                    r = time.time() - int(time_str[0:time_str.index('天前')]) * 60 * 60 * 60
                    return int(r)
                elif '小时前' in time_str:
                    r = time.time() - int(time_str[0:time_str.index('小时前')]) * 60 * 60 
                    return int(r)

if __name__ == "__main__":
    s_1 = "3分钟前"
    s0 = "3小时前"
    s1 = "30分钟前"
    s2 = "2016-03-01 15:30   "
    s6 = "2016-03-01"
    s4 = "2016年03月01日   "
    s3 = "2天前"
    print transtime(s6)
