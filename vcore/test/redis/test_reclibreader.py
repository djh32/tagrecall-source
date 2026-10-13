# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 10:36 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_reclibreader.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.redis.reclibreader import ReclibReader

if __name__ == "__main__":

    reader = ReclibReader(("rs52278.hebe.grid.sina.com.cn", 52278, 1))
    keys = reader.get_ts_keys(int(time.time() - 3 * 24 * 3600), int(time.time()))
    print(keys)

    mid2score = reader.get_mids(int(time.time() - 10 * 24 * 3600), int(time.time() - 8 * 24 * 3600))
    print(len(mid2score))
    count = 0
    for mid, score in mid2score.items():
        print(mid, score)
        count += 1
        if count > 20:
            break
