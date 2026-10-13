# _*_ coding: utf-8 _*_
# @Time    : 2020/7/22 11:45 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_simauthor_reader.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.redis.simauthorreader import SimAuthorReader

if __name__ == "__main__":
    reader = SimAuthorReader()
    authors = {"1000890063", "2949338000", "5747746655", "2354453684", "6135021919"}
    result = reader.load_sim2authors(authors)
    print(result)