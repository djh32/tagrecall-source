# _*_ coding: utf-8 _*_
# @Time    : 2019/10/31 5:33 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_tagcodetool.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time

from vcore.python.features.tagcodetool import TagcodeTool

if __name__ == "__main__":

    tool = TagcodeTool()
    print(tool.get_wbtag_name(["1042015:newAbilityTag_014002", "1042015:internetCompany_10000772"]))

    print(tool.get_tagid(["3009", "113734", "101"]))
    print(tool.get_tagname(["3009", "113734", "101"]))