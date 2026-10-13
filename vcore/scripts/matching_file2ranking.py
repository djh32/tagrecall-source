# _*_ coding: utf-8 _*_
# @Time    : 2019/12/20 2:20 PM

import pdb
import os
import sys
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../vcore/python/titan/')))
from vcore.python.titan.recallclient import RecallClient
from vcore.python.titan.titanclient import TitanClient

UID = "2085241395"
MODEL = "tab_gbdt_olduser_abtest_5"
TITAN = "10.93.187.200:10107"




def matching_line2ruf_response(matching_results_line, matching_client, model="tab_gbdt_olduser_abtest_5"):
    matching_results = matching_results_line.split(",")
    uid = matching_results[0]
    mids = matching_results[1:]

    _, _, jsondata_template = rclient.tab_recall(uid, page=1)
    #print(jsondata_template)

    matching_num = min(len(jsondata_template["cand"]), len(mids))
    print(matching_num)
    mids = mids[:matching_num]
    
    #pdb.set_trace()
    jsondata_template["model"] = model
    for i in range(matching_num):
        mid = mids[i]
        jsondata_template["cand"][i]["mid"] = mid
        recom_code = "1251"
        fake_aid = "0"
        jsondata_template["cand"][i]["recom_code"] = recom_code
        jsondata_template["cand"][i]["feature"]["recom_code"] = recom_code
        jsondata_template["cand"][i]["authorid"] = fake_aid
        jsondata_template["cand"][i]["aid"] = fake_aid
        jsondata_template["cand"][i]["feature"]["aid"] = fake_aid

    jsondata_template["cand"] = jsondata_template["cand"][:len(mids)]
    #print(jsondata_template["cand"])
    #print(len(jsondata_template["cand"]))

    jsondata = jsondata_template
    #print(jsondata)
    mid2info = {}
    context = {}
    cand = jsondata.get("cand", [])
    for item in cand:
        mid = item["mid"]
        feature = item.get("feature", {})
        mid2info[mid] = feature

    ctx = jsondata.get("context", {})
    for item in ctx.get("feat", []):
        context[item["fid"]] = item["val"]
    context["sessid"] = jsondata.get("sessid", "")
    context["bid"] = jsondata.get("bid", "")
    context["model"] = jsondata.get("model", "")


    return mid2info, context, jsondata 





if __name__ == "__main__":

    rclient = RecallClient()
    matching_results_line = open("./matching_file.txt").readline()
    #print(matching_results_line)
    mid2feas, context, jsondata = matching_line2ruf_response(matching_results_line, rclient, "tab_gbdt_olduser_abtest_5")
    #print(mid2feas)

    # Calling titan
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


