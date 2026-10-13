# _*_ coding: utf-8 _*_
# @Time    : 2019/9/27 3:02 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_openapis.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from vcore.python.utils.openapis import OpenApis

if __name__ == "__main__":

    apis = OpenApis()

    mids = ",".join(["4429664301287499", "4429663260947859"])
    ret = apis.statuses_showbatch(mids)
    print(ret)

    uids = ",".join(["1111681197", "1401659004"])
    ret = apis.user_showbatch(uids)
    print(ret)