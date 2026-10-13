# _*_ coding: utf-8 _*_
# @Time    : 2019/11/18 3:08 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_black_demo.py
#
# 黑灯流的demo 从召回到排序

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../vcore/python/titan/')))
import time

from vcore.python.titan.recallclient import RecallClient
from vcore.python.titan.titanclient import TitanClient

if __name__ == "__main__":

    smid = "4439295278065207"
    uid = "2085241395"

    rclient = RecallClient()
    mid2info, context, jsondata = rclient.black_recall(smid, uid)
    print(context)

    print("recall end.")

    mid2feas = {}
    for mid, info in mid2info.items():
        feas = info.get("feature", {})
        mid2feas[mid] = feas

    tclient = TitanClient("10.85.132.234", "5100")
    retfid = ["recom_code", "tmp_filter"]
    #retfid = ["recom_code"]
    ret = tclient.midrank("1111", "111111", "gbdt_101401_time_normal_neg", smid, uid, mid2feas, context, 100, retfid=retfid)
    print(ret)
