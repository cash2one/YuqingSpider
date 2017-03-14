# !/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wtq'

import re
import time, jieba, collections, os, csv
import Levenshtein as lst

''' Global const variable '''
g_defaultSpeed = 10000.0  # Speed threshold.
g_numOfMinTitles = 10  # Min number of title to calculate speed 低于这个数量的类，不计算速度
g_numOfShowTitles = 10  # The number of titles to show

# Load user dictionary
current_path = os.path.dirname(__file__)
jieba.load_userdict(current_path + "/CutWord/dict/dict.txt.big")

# Set stop words
stop_file = open(current_path + '/CutWord/dict/stop_word.txt', 'rb').read().decode('utf-8')
stop_word = set((u"。"))
for stop_file_words in stop_file.splitlines():
    stop_word.add(stop_file_words.strip())


class NewsCluster:
    def __init__(self, title, timestamp, itemId):
        '''
        :type title: str
        :type timestamp: float
        :type itemId: str
        '''
        self.m_titles = title  # First title in the cluster, and it will be the center of the cluster
        self.m_allTitles = [title]  # all titles in the cluster
        self.m_allItemsId = [itemId]  # The index is corresponding to m_allTitles
        self.m_startTime = timestamp  # use timestamp
        self.m_endTime = timestamp
        self.m_speed = g_defaultSpeed  # default is 1000
        self.m_num = 1.0  # number of article

    def update(self, timestamp, title):
        '''
        :type timestamp: str
        :type title: flaot
        '''
        self.m_startTime = min(self.m_startTime, timestamp)
        self.m_endTime = max(self.m_endTime, timestamp)
        self.m_num += 1

    def getSpeed(self):
        self.m_speed = (self.m_endTime - self.m_startTime) / self.m_num
        self.m_speed = (self.m_speed / 1000.0) / 60.0
        if self.m_speed <= 0 or self.m_num < g_numOfMinTitles: self.m_speed = g_defaultSpeed


''' Detect accident event '''


class AccidentEvent:
    def __init__(self):
        self.m_list = []  # restore news event.
        self.isOld = True  # whether the news is a new accident

    ''' !!! 暂时读本地文件，这里改成你读区文件的方式吧'''

    def readData(self, filePath):
        '''
        :filePath: str
        :rtype:	[]
        '''
        titles = []
        with open(filePath) as csvfile:
            reader = self.unfussy_reader(csv.reader(csvfile))
            for row in reader:
                titles.append(
                    row[6] + '::' + row[3] + '::' + row[0])  # row[6] is title, row[3] is time, row[0] is itemId ?
        return titles

    def unfussy_reader(self, csv_reader):
        '''
        Help readData() to skip wrong data
        '''
        while True:
            try:
                yield next(csv_reader)
            except csv.Error:
                continue

    def processTitle(self, title):
        '''
        Delete useless characters in title
        '''
        seg_list = jieba.cut(title.strip())
        newTitle = ''
        for ele in seg_list:
            if ele not in stop_word: newTitle += ele.strip()
        return newTitle

    def accidentEventDetection(self):

        if len(self.m_list) == 0:
            self.getClustersResult()
        # Sorted by speed
        ret_list, count = [], 1
        for ele in self.m_list:
            ele.getSpeed()
            ret_list.append((ele.m_allTitles, ele.m_speed, ele.m_titles))
        '''
        ret[0] is the cluster of titles
        ret[1] is the speed of the cluster
        '''
        ret = sorted(ret_list, key=lambda ret: ret[1])
        # print len(ret)
        keyword_and_rate = []
        for ele in ret:
            temp_list = []
            #topNWords = self.getEventKeywords2(ele[0], 5)
            topNWords = self.getEventKeywords(ele[0], 5)

            ''' Print the result accident event'''
            temp_list.append(topNWords)
            temp_list.append(round(ele[1], 2))
            temp_list.append(ele[2])
            keyword_and_rate.append(temp_list)
            # keyword_and_rate.append(ele[2])
            # print '# ' + str(count) + ' ' + topNWords + ' rate: ' + str(ele[1]) + ' min/news'
            count += 1
            if count > g_numOfShowTitles: break
        return keyword_and_rate

    def isSimilar(self, str1, str2):
        '''
        :type str1: str
        :type str2: str
        :rtype: boolean
        '''
        dis = lst.distance(str1, str2)
        ra = lst.ratio(str1, str2)
        if dis < 65 and ra > 0.25: return True
        return False

    def getEventKeywords(self, clusterList, numOfKey):
        '''
        Method1 : cut keywords

        Result formate: keyword1:weight1, keyword2:weight2, ..., speed XXX (news/min)
        :type clusterList: []
        :type numOfKey: int
        :rtype : string
        '''
        ret, ret_str, ret_list, countRet = {}, '', [], 0
        for ele in clusterList:
            seg_list = jieba.cut(ele, cut_all=False)
            for seg in seg_list:
                if seg not in stop_word:
                    if not re.search('[0-9]', seg):
                        if len(ret) == 0 or seg not in ret.keys():
                            ret[seg] = 1
                        else:
                            ret[seg] += 1
        # Unsorted
        for key in ret.keys():
            ret_list.append((key, ret[key]))
        # Sorted descending
        key_word = []
        ret_sorted = sorted(ret_list, key=lambda ret_list: ret_list[1])
        if len(ret_sorted) > numOfKey:
            for i in range(len(ret_sorted) - 1, len(ret_sorted) - numOfKey - 1, -1):
                temp = []
                temp.append(ret_sorted[i][0])
                temp.append(ret_sorted[i][1])
                key_word.append(temp)
                ret_str += ret_sorted[i][0] + ":" + str(ret_sorted[i][1]) + " "
        else:
            for i in range(len(ret_sorted) - 1, 0, -1):
                temp = []
                temp.append(ret_sorted[i][0])
                temp.append(ret_sorted[i][1])
                key_word.append(temp)
                ret_str += ret_sorted[i][0] + ":" + str(ret_sorted[i][1]) + " "

        # return ret_str
        return key_word

    def getEventKeywords2(self, clusterList, numOfKey):
        '''
        Method2
        '''
        ret_dic, ret_list, ret_str, = {}, [], ''
        for i in range(0, len(clusterList) - 1):
            for j in range(i + 1, len(clusterList)):
                tempStr = self.find_lcseque(clusterList[i], clusterList[j])
                # One CN character has 3 bytes
                if len(tempStr) >= 6 and len(tempStr) <= 18:
                    if len(ret_dic) == 0 or tempStr not in ret_dic.keys():
                        ret_dic[tempStr] = 1
                    else:
                        ret_dic[tempStr] += 1

        for key in ret_dic.keys():
            ret_list.append((key, ret_dic[key]))

        ret_sorted = sorted(ret_list, key=lambda ret_list: ret_list[1])
        key_word = []
        if len(ret_sorted) > numOfKey:
            for i in range(len(ret_sorted) - 1, len(ret_sorted) - numOfKey - 1, -1):
                temp = []
                temp.append(ret_sorted[i][0])
                temp.append(ret_sorted[i][1] * 2)
                key_word.append(temp)
                ret_str += ret_sorted[i][0] + ":" + str(ret_sorted[i][1] * 2) + " "
        else:
            for i in range(len(ret_sorted) - 1, 0, -1):
                temp = []
                temp.append(ret_sorted[i][0])
                temp.append(ret_sorted[i][1] * 2)
                key_word.append(temp)
                ret_str += ret_sorted[i][0] + ":" + str(ret_sorted[i][1] * 2) + " "
        if len(ret_str) == 0:
            return self.getEventKeywords(clusterList, numOfKey)
        # return ret_str
        return key_word

    def find_lcseque(self, s1, s2):
        '''
        Find the longest common subsequence
        '''
        col_size, row_size = len(s2)/3, len(s1)/3
        index_i,index_j = 0,0
        # Restore match result
        m = [ [ 0 for cols in range(col_size + 1)] for rows in range(row_size + 1) ] 
        # Record move direction
        d = [ [ None for cols in range(col_size + 1) ] for rows in range(row_size + 1) ] 

        for p1 in range(row_size):
            index_j = 0 
            for p2 in range(col_size): 
                if s1[index_i:index_i+3] == s2[index_j:index_j+3]:
                    m[p1+1][p2+1] = m[p1][p2]+1
                    d[p1+1][p2+1] = 'ok'          
                elif m[p1+1][p2] > m[p1][p2+1]:  
                    m[p1+1][p2+1] = m[p1+1][p2] 
                    d[p1+1][p2+1] = 'left'          
                else:                           
                    m[p1+1][p2+1] = m[p1][p2+1]   
                    d[p1+1][p2+1] = 'up'
                index_j += 3
            index_i += 3
        (p1, p2) = (row_size, col_size) 
        s = []
        index_i = 0
        while m[p1][p2]:    
            c = d[p1][p2]
            index_i = p1*3
            if c == 'ok':   
                s.append(s1[index_i-3:index_i])
                p1-=1
                p2-=1 
            if c =='left':  
                p2 -= 1
            if c == 'up':   
                p1 -= 1
        s.reverse() 
        return ''.join(s)

    def getClustersResult(self, titles):
        '''
        突发事件检测时，产生的聚类结果可直接使用
        '''
        # Count number of event
        for ele in titles:
            # tempStr[0] is title, tempStr[1] is time, tempStr[2] is itemId
            tempStr = ele
            # change data to timestamp
            timestamp = time.mktime(time.strptime(str(tempStr[1]), '%Y-%m-%d %H:%M:%S'))
            self.isNew = False
            # Cluster titles
            if len(self.m_list) == 0:
                news = NewsCluster(tempStr[0], timestamp, tempStr[2])
                self.m_list.append(news)
            else:
                for ele in self.m_list:
                    if self.isSimilar(ele.m_titles, tempStr[0]):
                        ele.update(timestamp, tempStr[0])
                        ele.m_allTitles.append(tempStr[0])
                        ele.m_allItemsId.append(tempStr[2])
                        self.isNew = True
                        break
                if not self.isNew:
                    news = NewsCluster(tempStr[0], timestamp, tempStr[2])
                    self.m_list.append(news)

        print 'The number of clusters: ' + str(len(self.m_list))
        class_id_list = []
        for cluster in self.m_list:
            temp_list = []
            for itemIndex in range(len(cluster.m_allTitles)):
                temp_list.append(cluster.m_allItemsId[itemIndex])
            class_id_list.append(temp_list)
            # print cluster.m_allTitles[itemIndex]+', '+cluster.m_allItemsId[itemIndex]
        return class_id_list

# t = AccidentEvent()
# t.accidentEventDetection()
# t.getClustersResult()  # 必需先执行accidentEventDetection，才可以调用这个函数，否则没有结果输出
