#!/usr/bin/env python
# -*- coding:utf-8 -*- 
__author__ = "liukang"

from StringIO import StringIO
import gzip
import cPickle

import sys
import time

from compress.data import data

def compress(data):
    fs = StringIO()
    gz = gzip.GzipFile(mode='wb',fileobj=fs)
    buff = cPickle.dumps(data)
    gz.write(buff)
    gz.close()
    res = fs.getvalue()
    fs.close()
    return res

def decompress(data):
    try:
        fs = StringIO(data)
        gz = gzip.GzipFile(fileobj=fs)
        buff = gz.read()
        res = cPickle.loads(buff)
    except:
        res = None
    gz.close()
    fs.close()
    return res


if __name__ == '__main__':
    print 'data_size:%s'%(sys.getsizeof(data))
    t0 = int(time.time())
    reuslt = compress(data)
    t1 = int(time.time())
    print 'result_size：%s'%(sys.getsizeof(reuslt))
    print '花费时间：%s' % (t1 - t0)