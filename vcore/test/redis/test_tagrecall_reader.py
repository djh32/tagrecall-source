# _*_ coding: utf-8 _*_
# @Time    : 2019/10/28 3:08 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_tagrecall_reader.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.redis.tagrecallreader import TagRecallReader

if __name__ == "__main__":

    reader = TagRecallReader("pkm25878.eos.grid.sina.com.cn", 25878, 0)
    print(reader.get_tag_mids("4420198112732240", version="v1"))