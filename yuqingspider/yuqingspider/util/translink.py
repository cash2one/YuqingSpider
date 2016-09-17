#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import urllib

def translink(link,url):
    if 'http' not in link[0]:
        proto,rest = urllib.splittype(url)
        host,rest=urllib.splithost(rest)
        if '/'==link[0][0]:
            link[0]='http://'+host+link[0]
        else:
            link[0]='http://'+host+'/'+link[0]
        return link
    else:
        return link

