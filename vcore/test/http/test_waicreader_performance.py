# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 6:10 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_waicreader_performance.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.redis.reclibreader import ReclibReader
from vcore.python.http.waicreader import WAICReader

if __name__ == "__main__":

    reader = ReclibReader(("rs52278.hebe.grid.sina.com.cn", 52278, 1))
    mid2score = reader.get_mids(int(time.time() - 10 * 24 * 3600), int(time.time() - 9.5 * 24 * 3600))
    print("mid num: ", len(mid2score))

    midlist = list(mid2score.keys())
    fidlist = ["10482", "10483", "10484", "10587", "10588", "10589", "10623", "10624", "10625"]

    wreader = WAICReader()

    startts = time.time()
    result = wreader.read_mid_feas(midlist, fidlist)
    endts = time.time()
    print("one-thread cost time: ", endts - startts, " secs.")
    print("valid mids: ", len(result))

    startts = time.time()
    result = wreader.mt_read_mid_feas(midlist, fidlist, 20)
    endts = time.time()
    print("multi-thread cost time: ", endts - startts, " secs.")
    print("valid mids: ", sum([len(i) for i in result]))




