# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 6:10 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_waicreader.py

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
    midlist = midlist[0:10]
    fidlist = ["10482", "10483", "10484", "10587", "10588", "10589", "10623", "10624", "10625"]
    fidlist = ["10539", "10650", "10570", "10483", "10484", "10587", "10616", "10617", "10618", "10620", "10626"]

    wreader = WAICReader()
    startts = time.time()
    result = wreader.mt_read_mid_feas(midlist, fidlist, 10)
    endts = time.time()
    print("multi-thread cost time: ", endts - startts, " secs.")
    print(result)

    uids = ["1111681197", "2085241395"]
    fidlist = ["21247", "21240", "21241", "21242"]
    result = wreader.read_uid_feas(uids, fidlist)
    print(result)





