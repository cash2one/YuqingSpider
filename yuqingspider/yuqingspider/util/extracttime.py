 #!/usr/bin/env python
 # -*- coding:utf-8 -*-
import re

def extracttime(str):
    l=re.findall('[^\x00-\xff]+',str)

    if len(l)==1:
        start=len(l[0])
        length=len(str)
        for i in range(start,length):
            if str[i]=='2':
                time=str[i:]
                return time
    else:
        time=str
        return time
