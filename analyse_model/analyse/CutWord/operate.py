# coding=utf-8
import os
import jieba, collections
# 加载自定义词典
current_path = os.path.dirname(__file__)
jieba.set_dictionary(current_path + '/dict/dict.txt.big')

g_company = [u'吉林石化', u'锦州石化', u'广西石化', u'长庆石化', u'兰州石化', u'大庆石化', u'克拉玛依', u'大连石化', u'大港石化', u'华北石化 ', u'中石油',
             u'中国石油四川销售', u'四川石化', u'辽宁石化']


def read_text(filepath):
    """
    :type filepath: str
    :rtype : str
    """
    file_text = open(filepath, 'r')
    mystr = ''
    for line in file_text:
        mystr += line
    return mystr


def locCutWords(article):
    """
    :type article: str
    :rtype : str
    """
    key_file = open(current_path + '/dict/mydic.txt', 'rb').read().decode('utf-8')
    key_word = set((u""))
    for key_file_words in key_file.splitlines():
        key_word.add(key_file_words.strip())

    seg_list = jieba.cut(article, cut_all=False)
    ret = ''
    for seg in seg_list:
        if seg in key_word: ret += seg + ' '
    return ret


def area_analysis(keywords):
    """
    :type keywords: str
    :rtype : str
    """
    words_box = []  # count and rank key words
    words_box.extend(keywords.strip().split())
    ranklist = collections.Counter(words_box)
    dic_keys = ranklist.keys()
    # handle special key words
    # 吉林石化
    if g_company[0] in dic_keys:
        ranklist[u'陕西'] = ranklist[u'陕西'] + ranklist[g_company[0]]
        ranklist[u'吉林'] = ranklist[u'吉林'] + ranklist[g_company[0]]
        del ranklist[u'吉林石化']
    # 锦州石化
    if g_company[1] in dic_keys:
        ranklist[u'锦州'] = ranklist[u'锦州'] + ranklist[g_company[1]]
        ranklist[u'辽西走廊'] = ranklist[u'辽西走廊'] + ranklist[g_company[1]]
        del ranklist[u'锦州石化']
    # 广西石化
    if g_company[2] in dic_keys:
        ranklist[u'广西'] = ranklist[u'广西'] + ranklist[g_company[2]]
        del ranklist[u'广西石化']
    # 长庆石化
    if g_company[3] in dic_keys:
        ranklist[u'咸阳'] = ranklist[u'咸阳'] + ranklist[g_company[3]]
        ranklist[u'鄂尔多斯'] = ranklist[u'鄂尔多斯'] + ranklist[g_company[3]]
        del ranklist[u'长庆石化']
    # 兰州石化
    if g_company[4] in dic_keys:
        ranklist[u'西部'] = ranklist[u'西部'] + ranklist[g_company[4]]
        ranklist[u'兰州'] = ranklist[u'兰州'] + ranklist[g_company[4]]
        del ranklist[u'兰州石化']
    # 大庆石化
    if g_company[5] in dic_keys:
        ranklist[u'大庆'] = ranklist[u'大庆'] + ranklist[g_company[5]]
        del ranklist[u'大庆石化']
    # 克拉玛依
    if g_company[6] in dic_keys:
        ranklist[u'黑油山'] = ranklist[u'黑油山'] + ranklist[g_company[6]]
        ranklist[u'准葛尔'] = ranklist[u'准葛尔'] + ranklist[g_company[6]]
        ranklist[u'独山子'] = ranklist[u'独山子'] + ranklist[g_company[6]]
        ranklist[u'新疆'] = ranklist[u'新疆'] + ranklist[u'黑油山'] + ranklist[u'准葛尔'] + ranklist[u'独山子']
        del ranklist[u'克拉玛依']
    # 大连石化
    if g_company[7] in dic_keys:
        ranklist[u'大连'] = ranklist[u'大连'] + ranklist[g_company[7]]
        ranklist[u'黄海'] = ranklist[u'黄海'] + ranklist[g_company[7]]
        del ranklist[u'大连石化']
    # 大港石化
    if g_company[8] in dic_keys:
        ranklist[u'天津'] = ranklist[u'天津'] + ranklist[g_company[8]]
        ranklist[u'渤海'] = ranklist[u'渤海'] + ranklist[g_company[8]]
        del ranklist[u'大港石化']
    # 华北石化
    if g_company[9] in dic_keys:
        ranklist[u'河南'] = ranklist[u'河南'] + ranklist[g_company[9]]
        del ranklist[u'华北石化']
    # 中石油
    if g_company[10] in dic_keys:
        ranklist[u'北京'] = ranklist[u'北京'] + ranklist[g_company[10]]
        del ranklist[u'中石油']
    # 中国石油四川销售
    if g_company[11] in dic_keys:
        ranklist[u'四川'] = ranklist[u'四川'] + ranklist[g_company[11]]
        del ranklist[u'中国石油四川销售']
    # 四川石化
    if g_company[12] in dic_keys:
        ranklist[u'内江'] = ranklist[u'内江'] + ranklist[g_company[12]]
        ranklist[u'成都'] = ranklist[u'成都'] + ranklist[g_company[12]]
        ranklist[u'都江堰'] = ranklist[u'都江堰'] + ranklist[g_company[12]]
        ranklist[u'四川'] = ranklist[u'四川'] + ranklist[u'内江'] + ranklist[u'成都'] + ranklist[u'都江堰']
        del ranklist[u'四川石化']
    # 辽宁石化
    if g_company[13] in dic_keys:
        ranklist[u'沈阳'] = ranklist[u'沈阳'] + ranklist[g_company[13]]
        del ranklist[u'辽宁石化']
    maxCity, maxCount = '无', 0
    for ele in ranklist:
        # print ele+','+str(ranklist[ele])
        if ranklist[ele] > maxCount: maxCity, maxCount = ele, ranklist[ele]
    return maxCity


def sentiment_analysis(article):
    i = 0

    # 设置关键词库
    word_file_neg = open(current_path + '/dict/neg_sentiment.txt', 'rb').read().decode('utf-8')
    neg_word = set((u""))
    for neg_file_words in word_file_neg.splitlines():
        neg_word.add(neg_file_words.strip())
    # 分词
    operate_wordlist = jieba.cut(article, cut_all=False)
    operate_cut_word = ''
    # 去除停用词
    for operate_word in operate_wordlist:
        if operate_word in neg_word:
            operate_cut_word = operate_cut_word + operate_word + '\t'
            i += 1

    if i > 5:
        return 'negative'
    else:
        return 'positive'


def content_analyse(article=None):
    # article = read_text('dict/test.txt')
    cur_text = locCutWords(article)
    area = area_analysis(cur_text)
    sentiment = sentiment_analysis(article)
    return [sentiment, area]


# a = content_analyse('我是四川石化人')
# print a[0]
# print a[1]
