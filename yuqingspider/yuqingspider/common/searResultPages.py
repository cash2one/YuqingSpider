__author__ = 'tanlong'

import urllib
from searchEngines import SearchEngines
from searchEngines import TurnPageByCount


class searResultPages:
    totalPage = 0
    keyword = None,
    searchEngineUrl = None
    currentPage = 1
    searchEngine = None

    def __init__(self, keyword, url, totalPage, type_page):
        self.type_page = type_page
        # self.searchEngine = searchEngine.lower()
        # self.searchEngineUrl = SearchEngines[self.searchEngine]
        self.searchEngineUrl = url
        self.totalPage = totalPage
        self.keyword = keyword
        print "total page:{0}".format(self.totalPage)

    def __iter__(self):
        return self

    def _currentUrl(self):
        if self.type_page:
            # 1 page by 10
        # if self.searchEngine in TurnPageByCount:
            return self.searchEngineUrl.format(self.keyword, str((self.currentPage - 1) * 10))
        # elif 'weibo' in self.searchEngine:
        #     print 'self.keyword:%s' % self.keyword
        #     return self.searchEngineUrl.format(urllib.quote(str(self.keyword)), str(self.currentPage))
        else:
            return self.searchEngineUrl.format(self.keyword, str(self.currentPage))

    def next(self):
        if self.currentPage <= self.totalPage:
            url = self._currentUrl()
            self.currentPage = self.currentPage + 1
            return url
        raise StopIteration
