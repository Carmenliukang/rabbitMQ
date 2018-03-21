#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

import urlparse

import simplejson

http = 'http://tool.oschina.net/encode?'
url = "salesPlatformOrderNo=20180319025828341097&amp;invoiceTitle=%E4%B8%AA%E4%BA%BA&amp;goodsNo=EMG4418048348210%2CEMG4418046703900&amp;sellerRemark=%E3%80%903-19%E4%B8%AD%E8%A1%8C%E6%96%B0%E5%90%8E%E5%8F%B0%E8%AE%A2%E5%8D%95%E3%80%91%E5%88%86%E6%9C%9F%E6%95%B012%E5%95%86%E5%93%81%E7%BC%96%E5%8F%B7LSSM171217P027%E6%80%BB%E9%87%91%E9%A2%9D960%E6%80%BB%E7%A7%AF%E5%88%860+%E3%80%903-19+13%E7%82%B919%E5%88%8648%E7%A7%92%E3%80%91%E3%80%90%E9%9C%80%E6%94%AF%E4%BB%98%E3%80%91&amp;insuredValue=0.000&amp;orderMark=00000000000000000000000000000000000000000000000000&amp;addressCounty=%E5%85%AD%E5%90%88%E5%8C%BA&amp;shopNo=ESP0020000009400&amp;consigneeMobile=16651619010&amp;salePlatformSource=6&amp;consigneeAddress=%E6%B1%9F%E8%8B%8F%E5%8D%97%E4%BA%AC%E5%B8%82%E5%85%AD%E5%90%88%E5%8C%BA%E9%A9%AC%E9%9E%8D%E6%9C%BA%E5%9C%BA&amp;format=json&amp;timestamp=2018-03-21+14%3A37%3A58&amp;shipperNo=CYS0000010&amp;addressProvince=%E6%B1%9F%E8%8B%8F&amp;access_token=82c43baa-7c6c-45b0-8b3e-3f85a730eb53&amp;billType=OUT_SALE&amp;insuredPriceFlag=0&amp;isvSource=ISV0020000000137&amp;v=2.0&amp;invoiceContent=%E4%B8%AA%E4%BA%BA&amp;consigneeName=%E6%9D%8E%E5%B7%9D&amp;sign=04353C31A519C9D97F4DAB2BCC15B735&amp;consigneeRemark=%E5%AE%A2%E6%88%B7%E6%9D%A5%E7%94%B5%E5%82%AC%E5%8F%91%E8%B4%A7%EF%BC%8C%E9%BA%BB%E7%83%A6%E5%B0%BD%E5%BF%AB%E5%A4%84%E7%90%86%E2%80%94%E2%80%94TJ+%E5%BC%A0%E5%A5%A5%0A&amp;orderPrice=960&amp;isvUUID=1803212000182&amp;method=jingdong.eclp.order.addOrder&amp;receivable=0&amp;price=480%2C480&amp;app_key=AE478F9BEAB8979AD79A6F6A70988AA5&amp;addressCity=%E5%8D%97%E4%BA%AC%E5%B8%82&amp;departmentNo=EBU0000000006313&amp;warehouseNo=110006341&amp;quantity=1%2C1"

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
