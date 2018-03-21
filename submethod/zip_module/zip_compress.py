#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

import sys

sys.path.append('/demo')  # 用于增加包的路径
import zlib
import simplejson
import base64

from compress.data import data_dict


def compress(data):
    try:
        data_json = simplejson.dumps(data)
        # 将数据压缩成字节流
        json_compress = zlib.compress(data_json)
        # 对字节流进行64位编码，因为字节流传输不能导入到MQ中。
        result = base64.b64encode(json_compress)
        return result
    except Exception as e:
        print e
        return data


def decopress(data):
    try:
        data_64code = base64.b64decode(data)
        decopress_data = zlib.decompress(data_64code)
        result = simplejson.loads(decopress_data)
        return result

    except Exception as e:
        print e
        result = simplejson.loads(data)
        return result


if __name__ == '__main__':
    data = data_dict
    print '原数据：%s' % (data)
    compress_data = compress(data)
    print '压缩后的数据：:%s' % (compress_data)
    decopress_data = decopress(compress_data)
    print '解压后的数据：%s' % (decopress_data)
