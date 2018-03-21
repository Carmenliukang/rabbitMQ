#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "liukang"

import memcache

mc = memcache.Client(["locaohost:11211"])

def mc_get(id):
    try:
        result = mc.get(str(id))
        return result
    except:
        return 'fail'

def mc_delete(id_list):
    try:
        if type(id_list) == list:
            for key in id_list:
                mc.delete(key)
        else:
            mc.delete(str(id_list))
        return 'succ'

    except:
        return 'fail'


if __name__ == '__main__':
    id_list = [
        'rel_1734313036_store.trade.fullinfo.get_1054182434'
    ]

    id = 'rel_1048994536_store.trade.fullinfo.get_1054182434'

    mc_delete_id = mc_delete(id)

    mc_find_id = mc_get(id)
