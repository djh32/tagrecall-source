# _*_ coding: utf-8 _*_
# @Time    : 2019/11/18 3:08 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_tab_demo.py
#
# tab流的demo 从召回到排序

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../vcore/python/titan/')))
import time

from vcore.python.titan.recallclient import RecallClient
from vcore.python.titan.titanclient import TitanClient

if __name__ == "__main__":
    uid = "2085241395"

    rclient = RecallClient()
    mid2info, context, jsondata = rclient.tab_recall(uid, 2)
    print(jsondata.get("recall", {}))
    #print(context)
    #print(mid2info)
    #print("recall end.")
    #print("mid num: ", len(mid2info))

    #tclient = TitanClient("i.titan.recom.weibo.com", "5001")
    tclient = TitanClient("10.85.132.15", "10218")
    retfid = ["recom_code", "tmp_filter", "tmp_cgrank_type"]
    #retfid = ["recom_code"]
    ret = tclient.uidrank2("1111", "111111", "tab_gbdt_baseline_ctr_click_olduser_cgrank", uid, mid2info, context, 20, retfid=retfid)
    #ret = tclient.recallFm("4111",uid,"ruf_channel1","v1", context, 20)
    print(ret)
