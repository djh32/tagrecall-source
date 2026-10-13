# _*_ coding: utf-8 _*_
# @Time    : 2019/10/22 2:47 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_openapi_midreader.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.http.openapimidreader import MidReader
from vcore.python.redis.reclibreader import ReclibReader

if __name__ == "__main__":

    reader = MidReader()
    midlist = ["4429664301287499", "4429663260947859", "4429787642911302"]
    (videos, rawlist) = reader.get_videos(midlist)
    for v in videos:
        print(v)

    reader = ReclibReader(("rs52278.hebe.grid.sina.com.cn", 52278, 1))
    mid2score = reader.get_mids(int(time.time() - 10 * 24 * 3600), int(time.time() - 9.5 * 24 * 3600))
    print("mid num: ", len(mid2score))
    midlist = list(mid2score.keys())

    startts = time.time()
    result = MidReader.mt_get_videos(midlist, 10, 3)
    endts = time.time()
    print("multi-thread cost time: ", endts - startts, " secs.")
    print("valid mids: ", sum([len(i) for i in result]))
