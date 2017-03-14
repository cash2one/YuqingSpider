__author__ = 'tanlong'

import urllib
from searchEngines import SearchEngines
from searchEngines import TurnPageByCount


class searResultPages:
    totalPage = 0
    keyword = None,
    searchEngineUrl = None
    # currentPage = 1
    searchEngine = None

    def __init__(self, keyword, url, startPage, endPage, type_page, key_page_sort=1):
        self.type_page = type_page
        # self.searchEngine = searchEngine.lower()
        # self.searchEngineUrl = SearchEngines[self.searchEngine]
        self.currentPage = startPage
        self.searchEngineUrl = url
        self.endPage = endPage
        self.keyword = keyword
        self.key_page_sort = key_page_sort
        print "total page:{0}".format(self.endPage)

    def __iter__(self):
        return self

    def currentUrl(self):

        if self.key_page_sort:
            if self.type_page:
                # 1 page by 10
                return self.searchEngineUrl.format(self.keyword, str((self.currentPage - 1) * 10))
            # elif 'weibo' in self.searchEngine:
            #     print 'self.keyword:%s' % self.keyword
            #     return self.searchEngineUrl.format(urllib.quote(str(self.keyword)), str(self.currentPage))
            else:
                return self.searchEngineUrl.format(self.keyword, str(self.currentPage))

        else:
            if self.type_page:
                # 1 page by 10
                return self.searchEngineUrl.format(str((self.currentPage - 1) * 10), self.keyword)
            # elif 'weibo' in self.searchEngine:
            #     print 'self.keyword:%s' % self.keyword
            #     return self.searchEngineUrl.format(urllib.quote(str(self.keyword)), str(self.currentPage))
            else:
                return self.searchEngineUrl.format(str(self.currentPage), self.keyword)

    def next(self):
        if self.currentPage <= self.endPage:
            url = self.currentUrl()
            self.currentPage = self.currentPage + 1
            return url
        raise StopIteration
