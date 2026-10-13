# _*_ coding: utf-8 _*_
# @Time    : 2019/12/20 2:20 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_uidrank.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../vcore/python/titan/')))
from vcore.python.titan.recallclient import RecallClient
from vcore.python.titan.titanclient import TitanClient

UID = "2085241395"
MODEL = "tab_gbdt_1216_ctr_index_v2"
TITAN = "10.85.132.234:5102"

if __name__ == "__main__":

    # 获取召回内容
    rclient = RecallClient()
    mid2feas, context, jsondata = rclient.tab_recall(UID, page=1)
    if "model" in context and not MODEL:
        MODEL = context["model"]

    # 调用排序模型
    (host, port) = TITAN.split(":")
    tclient = TitanClient(host, port)
    retfid = ["recom_code", "tmp_filter"]
    result = tclient.uidrank(context.get("bid", "1111"), context.get("sessid", "11111"), MODEL, UID, mid2feas, context,
                             20,
                             retfid=retfid, debug=False)

    recmidlist = [mid for mid in result.id]
    scorelist = [score for score in result.score]

    for idx, mid in enumerate(recmidlist):
        print("mid:", mid, " score:", scorelist[idx])