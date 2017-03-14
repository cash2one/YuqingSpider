import re
import json
import requests 

def extract_from_search_response(response):
    print response.body
    script_text = re.findall('STK && STK.pageletM && STK.pageletM.view\({"pid":"pl_weibo_direct",(.*)}\)</script>', response.body)
    try:
        text = json.loads('{' + script_text[0] +'}')['html'].encode('utf8').replace(r'\"', r'"').replace(r'\/', r'/')
    except Exception, e:
        print e
        return response
    response = response.replace(body=text)
    return response

def extract_from_feed_response(response):
    print response.body 
    #script_text = re.findall('FM.view\({"ns":"pl.content.homeFeed.index","domid":"Pl_Official_MyProfileFeed__*",(.*)}\)</script>\n<script>FM.view\({"ns":"pl.content.timeBase.index"', response.body, re.DOTALL)
    script_text = re.findall('FM.view\({"ns":"pl.content.homeFeed.index","domid":"Pl_Official_MyProfileFeed__(.*)}\)</script>\n<script>FM.view\(', response.body, re.DOTALL)
    try:
        text = json.loads('{"num":"' + script_text[0] +'}')['html'].encode('utf8').replace(r'\"', r'"').replace(r'\/', r'/')
    except Exception, e:
        print e
    response = response.replace(body=text)
    return response

def extract_hot_list(response):
    print response.body
    url = 'http://m.weibo.cn/p/index?containerid=100803_-_page_hot_list'
    text = re.findall('window.\$render_data = (.*);</script><script src=', response.body, re.DOTALL)
    try:
        content = json.loads(text[0].replace('\'', '"'))
        maincontent = content['stage']['page'][1]['card_group'][0]['card_group'] 
        return maincontent
    except Exception, e:
        print e

def extract_from_feed1_response(response):
    script_set = response.xpath('//script')
    script = ''
    for s in script_set:
        try:
            s_text = s.xpath('text()').extract()[0].encode('utf8').replace(r'\"', r'"').replace(r'\/', r'/')
        except Exception,e:
            print e
            return response
        if s_text.find('WB_feed_detail') > 0:
            script = s_text
            break
    response = response.replace(body=s_text)
    return response

def extract_weibo_content(response, weibo_type = 'search'):
    if weibo_type == 'search':
        response = extract_from_search_response(response)
    elif weibo_type == 'hot':
        response = extract_hot_list(response)
    else:
        response = extract_from_feed_response(response)
    return response

if __name__ == '__main__':
    extract_hot_list()
