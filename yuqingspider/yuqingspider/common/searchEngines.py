__author__ = 'tanlong'

TurnPageByCount = ['baidu', 'youdao']

SearchEngines = {
    'baidu': 'http://news.baidu.com/ns?word={0}&pn={1}',
    'sogou': 'http://news.sogou.com/news?query={0}&page={1}',
    'sogoublog': 'http://www.sogou.com/web?query={0}&interation=196647&page={1}',
    'qihoo': 'http://news.so.com/ns?q={0}&pn={1}',
    'youdao': 'http://news.youdao.com/search?q={0}&start={1}',
    'weibosearch': 'http://s.weibo.com/weibo/{0}&page={1}',
    'weibocontent': 'http://weibo.com/u/{0}/?is_all={1}',
    'weibohot': 'http://m.weibo.cn/p/index?containerid=100803_-_page_hot_list{0}/{1}',
    'rqxx': 'http://bbs.rqxx.com.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'hc360':'http://zhannei.baidu.com/cse/search?q={0}&p={1}&click=1&s=1366092766520538444&nsid=', 
    'kdnet':'http://search.kdnet.net/?q={0}&sa=%CB%D1%CB%F7&category=title&boardid=0&arrival=2013-03-01&departure=2016-03-01&p={1}&m=705d8',
    'zhongsou':'http://bbs.zhongsou.com/b?w={0}&b={1}&s=0&sc=&pt=0&t=&dt=0&fo=&u=&au=&nt=1',
    'tianya':'http://search.tianya.cn/bbs?s=4&q={0}&pn={1}',
    'sunpetro':'http://www.sunpetro.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'oilhb':'http://bbs.oilhb.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'qinmin':'http://www.qinmin.cc/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'hcbbs':'http://bbs.hcbbs.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    '29nh':'http://nepu.29nh.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'oilequipcn':'http://www.oilequipcn.net/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'fracchina':'http://bbs.fracchina.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'hg707':'http://bbs.hg707.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'mahoupao':'http://bbs.mahoupao.net/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'jhyta':'http://www.jhyta.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'petroren':'http://www.petroren.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'baiduyun':'http://www.baiduyun.me/search.php?mod=forum&searchid={2}2&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'daxues':'http://www.daxues.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'mhg114':'http://www.mhg114.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'bucter':'http://www.bucter.com/bbs/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'youqiyunshu':'http://www.youqichuyun.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'myubbs':'http://upc.myubbs.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'oilsir':'http://www.oilsir.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'junzhuan':'http://bbs.junzhuan.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'ltaaa':'http://www.ltaaa.com/bbs/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'hainei':'http://so.hainei.org/cse/search?q={0}&p={1}&s=13490577094485005644&srt=cse_createTime&nsid=0&entry=1',
    'rednet':'http://bbs.rednet.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'cnr':'http://bbs.cnr.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'm4':'http://bbs.m4.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'haiwainet':'http://bbs.haiwainet.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'wandaclub':'http://www.wandaclub.cc/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'scol':'http://bbs.scol.com.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'yinxiangzg':'http://bbs.yinxiangzg.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'gmw':'http://bbs.gmw.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'sohu':'http://s.club.sohu.com/?action=search&type=0&keyword={0}&timeauto=1&page={1}',
    'fyjs':'http://www.fyjs.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    '23zhibo':'http://www.23zhibo.net/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'wj1818':'http://www.wj1818.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'nhjd':'http://www.nhjd.net/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    '9ifly':'http://www.9ifly.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page{1}',
    'lzszg':'http://bbs.lzszg.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'onefx':'http://www.onefx.net/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'wacai':'http://bbs.wacai.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'fx678':'http://my.fx678.com/search.php?mod=forum&searchid=32&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    '55168':'http://bbs.55168.cn/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'fxunion':'http://bbs.fxunion.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'bi22':'http://www.bi22.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'ruoshui':'http://bbs.ruoshui.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    '178448':'http://www.178448.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'gupiao168':'http://www.gupiao168.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'gupzs':'http://bbs.gupzs.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'jue-ce':'http://jue-ce.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'gushenbbs':'http://www.gushenbbs.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    'dqdaily':'http://bbs.dqdaily.com/search.php?mod=forum&searchid={2}&orderby=dateline&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
    '010':'http://bbs.010.cc/search.php?mod=forum&searchid={2}&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw={0}&page={1}',
}


SearchEngineResultSelectors= {
    'baidu': { 'block': '//div[@class="result"]', 'link': 'h3/a/@href', 'title': 'h3/a/text()', 'from': './/p[@class="c-author"]/text()', 'abstract':'string(div[contains(@class, "c-summary")]/text())'},
    'sogou': { 'block': '//div[@class="vrwrap"]', 'link': './/h3/a/@href', 'title': './/h3/a/text()', 'from': './/p[@class="news-from"]/text()', 'abstract':'string(.//p[@class="news-txt"]/span)'},
    'sogoublog': { 'block': '//div[@class="vrwrap"]', 'link': './/h3/a/@href', 'title': './/h3/a/text()', 'from': './/cite/text()', 'time':'.//cite/date/text()', 'abstract':'string(.//li[@class="str-text-info"])'},
    'qihoo': { 'block': '//li[contains(@class,"res-list")]', 'link': './/h3/a/@href', 'title': './/h3/a/text()', 'from': './/span[@class="sitename"]/text()', 'time':'.//span[@class="posttime"]/@data-pdate', 'abstract':'string(.//p[@class="content"])'},
    'youdao': { 'block': '//ul[@class="rz"]/li', 'link': './/h3/a/@href', 'title': 'string(.//h3/a)', 'from': './/span[@class="green stat"]//text()', 'abstract':'.//p/text()'},
    'rqxx': {'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'.//h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'hc360':{'block':'//div[@class="result f s3"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//div[@class="c-summary-1"]/span[1]/text()','abstract':'.//div/div/div/text()','answerandlookup':'.//div[@class="c-summary-1"]/span[4]/text()','time':'.//div[@class="c-summary-1"]/span[3]/text()','author':'.//div[@class="c-summary-1"]/span[2]/text()'},
    'kdnet':{'block':'//div[@class="search-result-list"]','link':'h2/a/@href','title':'h2/a/text()','from':'h2/span/a/text()','abstract':'a/text()','answerandlookup':'span/span[@class="c-alarm"]/text()','time':'span[@class="c-sub"]/text()[3]','author':'span/span[@class="c-main"]/a/text()'},
    'zhongsou':{'block':'//ul[@class="bbs-list"]/li','link':'h3/a/@href','title':'h3/a/text()','from':'p[2]/a[2]/text()','abstract':'p[1]/text()','answerandlookup':'p[2]/text()[3]','time':'h3/span/text()','author':'p[2]/a[1]/text()'},
    'tianya':{'block':'//div[@class="searchListOne"]/ul/li','link':'.//div/h3/a/@href','title':'.//div/h3/a/text()','from':'.//p[@class="source"]/a[1]/text()','abstract':'.//div/p/text()','answerandlookup':'.//p[@class="source"]/span[2]/text()','time':'.//p[@class="source"]/span[1]/text()','author':'.//p[@class="source"]/span[2]/a/text()'},
    'sunpetro':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'oilhb':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'qinmin':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'hcbbs':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    '29nh':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'oilequipcn':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'fracchina':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'hg707':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'mahoupao':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'jhyta':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'petroren':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'baiduyun':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'daxues':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'mhg114':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'bucter':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'youqiyunshu':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'myubbs':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'oilsir':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'junzhuan':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'ltaaa':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'hainei':{'block':'//div[@class="result f s3"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//div[@class="c-summary-1"]/span[1]/text()','abstract':'.//div/div/div/text()','answerandlookup':'.//div[@class="c-summary-1"]/span[5]/text()','time':'.//div[@class="c-summary-1"]/span[3]/text()','author':'.//div[@class="c-summary-1"]/span[2]/text()'},
    'rednet':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'cnr':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'm4':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'haiwainet':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'wandaclub':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'scol':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'yinxiangzg':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'gmw':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'sohu':{'block':'//div[@class="resultItem"]','link':'h1/a/@href','title':'h1/a/text()','from':'.//a[2]/text()','abstract':'.//p/text()','answerandlookup':'h1/a/text()','time':'span[3]/text()','author':'a[1]/text()'},
    'fyjs':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    '23zhibo':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'wj1818':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'nhjd':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    '9ifly':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'lzszg':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'onefx':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'wacai':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'fx678':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    '55168':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'fxunion':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'bi22':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'ruoshui':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    '178448':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'gupiao168':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'gupzs':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'jue-ce':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'gushenbbs':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    'dqdaily':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
    '010':{'block':'//ul/li[@class="pbw"]','link':'h3/a/@href','title':'h3/a/text()','from':'.//p[3]/span[3]/a/text()','abstract':'.//p[2]/text()','answerandlookup':'.//p[1]/text()','time':'.//p[3]/span[1]/text()','author':'.//p[3]/span[2]/a/text()'},
}
