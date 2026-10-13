# _*_ coding: utf-8 _*_
# @Time    : 2019/11/18 3:08 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_black_demo.py
#
# vvs流的demo 从召回到排序

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../vcore/python/titan/')))
import time

from vcore.python.titan.recallclient import RecallClient
from vcore.python.titan.titanclient import TitanClient

if __name__ == "__main__":

    smid = "4476659229444108"
    uid = "2085241395"

    rclient = RecallClient()
    mid2info, context, jsondata = rclient.vvs_recall(smid, uid)
    print(context)

    print("recall end.")

    mid2feas = {}
    for mid, info in mid2info.items():
        feas = info.get("feature", {})
        #if feas["recom_code"] == "4036":
        #    feas["weight_score"] = "10"
        mid2feas[mid] = feas

    context["titan_recall_assign"] = "4036:5"

    tclient = TitanClient("10.85.132.217", "5234")
    retfid = ["recom_code", "tmp_filter"]
    #retfid = ["recom_code"]
    ret = tclient.midrank("1111", "111111", "vvs_gbdt_120301_time_clf", smid, uid, mid2feas, context, 20, retfid=retfid, debug=False)
    print(ret)
