#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

import urllib
import urlparse

import simplejson

http = 'http://tool.oschina.net/encode?'
url = urllib.urlencode({'name':'刘康','age':24})
# result = urllib.unquote(url)
# print result

# result = urllib.urlencode(url)
# print result

url_result = http + url
url_data = urlparse.urlsplit(url_result)
result = urlparse.parse_qs(urlparse.urlsplit(url_result).query)
print simplejson.dumps(result, ensure_ascii=False, indent=1)


def url_encode(url_data):
    http = 'http://locaohost:80/?'
    if 'http://' not in url_data:
        url_result = http + url_data
    else:
        url_result = url_data

    try:
        data = urlparse.parse_qs(urlparse.urlsplit(url_result).query)
        result = simplejson.dumps(data, ensure_ascii=False, indent=1)
        print '结果为：%s' % (result)
        return 'succ'

    except Exception as e:
        print 'error'
        return 'fail'
