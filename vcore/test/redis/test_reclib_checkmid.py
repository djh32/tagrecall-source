# _*_ coding: utf-8 _*_
# @Time    : 2020/1/25 10:45 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_reclib_checkmid.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.redis.reclibreader import ReclibReader

if __name__ == "__main__":

    reader = ReclibReader(("rs52278.hebe.grid.sina.com.cn", 52278, 1))
    mid = "4464708901803153"
    print(reader.check_mid(mid))