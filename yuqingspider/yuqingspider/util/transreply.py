#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import re

def transreply(str):
    l=re.findall('\d+',str)
    if len(l)>=2:
        if int(l[0])<int(l[1]):
            return l[0],l[1]
        else:
            return l[1],l[0]
    if len(l)==1:
        if int(l[0])>100:
            return '0',l[0]
        else:
            return l[0],l[0]
    if len(l)==0:
        return '0','0'

