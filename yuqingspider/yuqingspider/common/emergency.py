#!/usr/local/bin/python2.7
#coding:utf-8
__author__ = 'tanlong'


SearchEngines={
'huibeiyingji':'http://yj.hubei.gov.cn/yjbjy/',

'fm':'http://fm.m4.cn/events/' ,
'wubai':'http://www.bbaqw.com/shijian.htm',
'redianzixun':'http://www.ymylife.cn/shehui/shijian/ ',
'jinrixinwen':'http://www.05188.com/news/huati/ ',

'shijianzaixian':'http://www.event123.cn/junshi/9/  ',

'diandongredian':'http://www.d1ev.com/special-focus ',

'diandongzhuangti':'http://www.d1ev.com/special  ',

'shihuipingdao':'http://www.tj.xinhuanet.com/shpd/rdsj.htm  ',
'oknetshehui':'http://www.oknet.cc/shehuishijian/  ',
'oknetredian':'http://www.oknet.cc/guoneishijian/ ',
'oknetguoji':'http://www.oknet.cc/guojishijian/'
}

SearchEngineResultSelectors={
'huibeiyingji':{'block':'/html/body/div[5]/div[2]/ul/li','title':'a/text()','link':'a/@href','time':'span/text()'},
'fm':{'block':'//div[@class="articlelist0"]/div[@class="articleitem0 "]','title':'div/h3/a/text()','link':'div/h3/a/@href','time':'div/div/div/span/text()'},
'wubai':{'block':'//div[@class="incident-text"]/div[@class="incident-pic"]','title':'h3/a/text()','link':'h3/a/@href','time':'h3/span/text()'},

'redianzixun':{'block':'/html/body/div/div[4]/div[3]/div[1]/div[2]/div[3]/div[2]/ul/li','title':'h3/a/text()','link':'h3/a/@href','time':'h3/span/text()'},
'jinrixinwen':{'block':'//*[@id="wrapper"]/div[1]/div[2]/ul/li','title':'div/h2/a/text()','link':'h3/a/@href','time':'h3/span/text()'},
'shijianzaixian':
{'block':'//div[@class="listbox mt3"]/div','title':'h3/a/text()','link':'h3/a/@href'},
'diandongredian':
{'block':'/html/body/article/div[5]/ul/li','title':'div[1]/h3/a/text()','link':'div[1]/h3/a/@href'},
'diandongzhuangti':{'block':'/html/body/article/div[5]/ul/li','title':'div[1]/h3/a/text()','link':'div[1]/h3/a/@href'},

'shihuipingdao':{'block':'/html/body/div[5]/div[1]/div[1]/div[2]/div/ul/li','title':'div/a/text()','link':'div/a/@href','time':'div/span/text()'},
'oknetshehui':{'block':'//div[@class="content"]/div[@class="list"]','title':'dl/dt/a/text()','link':'dl/dt/a/@href','time':'dl/dt/span/text()'},
'oknetredian':{'block':'//div[@class="content"]/div[@class="list"]','title':'dl/dt/a/text()','link':'dl/dt/a/@href','time':'dl/dt/span/text()'},
'oknetguoji':{'block':'//div[@class="content"]/div[@class="list"]','title':'dl/dt/a/text()','link':'dl/dt/a/@href','time':'dl/dt/span/text()'}
}





