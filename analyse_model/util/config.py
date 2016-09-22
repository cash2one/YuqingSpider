__author__ = 'tanlong'

TurnPageByCount = ['baidu', 'youdao']

SearchEngines = {
    'baidu': 'http://news.baidu.com/ns?word={0}&pn={1}',
    'sogou': 'http://news.sogou.com/news?query={0}&page={1}',
    'qihoo': 'http://news.so.com/ns?q={0}&pn={1}',
    'youdao': 'http://news.youdao.com/search?q={0}&start={1}',
    'weibosearch': 'http://s.weibo.com/weibo/{0}&page={1}',
    'weibocontent': 'http://weibo.com/{0}/?is_all={1}',
    'weibohot': 'http://m.weibo.cn/p/index?containerid=100803_-_page_hot_list{0}/{1}',
}


SearchEngineResultSelectors= {
    'baidu': { 'block': '//div[@class="result"]', 'link': 'h3/a/@href', 'title': 'h3/a/text()', 'from': './/p[@class="c-author"]/text()', 'abstract':'string(div[contains(@class, "c-summary")]/text())'},
    'sogou': { 'block': '//div[@class="vrwrap"]', 'link': './/h3/a/@href', 'title': './/h3/a/text()', 'from': './/p[@class="news-from"]/text()', 'abstract':'string(.//p[@class="news-txt"]/span)'},
    'qihoo': { 'block': '//li[contains(@class,"res-list")]', 'link': './/h3/a/@href', 'title': './/h3/a/text()', 'from': 'string(.//p[@class="newsinfo"])', 'abstract':'string(.//p[@class="content"])'},
    'youdao': { 'block': '//ul[@class="rz"]/li', 'link': './/h3/a/@href', 'title': './/h3/a/text()', 'from': './/span[@class="green stat"]//text()', 'abstract':'.//p/text()'},
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = '123'
SPIDER_DB = 'yuqing'
