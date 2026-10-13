# _*_ coding: utf-8 _*_
# @Time    : 2019/11/18 2:32 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : recallclient.py
# 调用@向前给的demo接口，获取召回列表

import requests
import json
import urllib.parse

class RecallClient():

    def __init__(self):
        pass

    def dot_recall(self, uid):
        url = "http://10.182.9.194:6006/get_push_demo"

        remind_info = [{"remind_type":10001,"remain":2},{"remind_type":10002,"remain":10},{"remind_type":10004,"remain":1}]

        param = {}
        param["uid"] = uid
        param["remind_info"] = json.dumps(remind_info)
        param["from"] = "10B4195010"
        headers = {"Content-Type": "application/json"}

        result = requests.post(url, headers = headers, data = param).content.decode("utf-8")
        jsondata = json.loads(result)
        cand = jsondata.get("cand", [])
        mid2info = {}
        context = {}
        for item in cand:
            aids = item.get("aids")
            feature = item.get("feature", {})
            mid2info[aids] = feature

        ctx = jsondata.get("context")
        for item in ctx.get("feat", []):
            context[item["fid"]] = item["val"]

        context["sessid"] = jsondata.get('sessid', "")
        context["bid"] = jsondata.get("bid", "")
        context["model"] = jsondata.get("model", "")
        return mid2info, context, jsondata

    def black_recall(self, smid, uid, luicode="", page=1):
        '''
        调用黑灯流召回
        :param smid: 导流mid
        :param uid:
        :param luicode:
        :param page:
        :return:
        '''
        url = "http://10.85.132.42:6006/demo_horizental?mid={0}&uid={1}&luicode={2}&page={3}".format(smid, uid, luicode, page)
        print(url)
        headers = {}
        content = requests.get(url, headers=headers, timeout=3)

        jsondata = content.json()
        mid2info = {}
        context = {}
        for k,v in jsondata.items():
            if k == "context":
                context = v
            elif k.isdigit():
                mid = v["mid"]
                mid2info[mid] = v
            else:
                pass

        return mid2info, context, jsondata

    def vvs_recall(self, smid, uid, page=1):
        '''
        调用vvs流召回
        :param smid: 导流mid
        :param uid:
        :param luicode:
        :param page:
        :return:
        '''
        url = "http://10.85.132.42:6006/demo_vertical?mid={0}&uid={1}&pid=921&page={2}".format(smid, uid, page)
        print(url)
        headers = {}
        content = requests.get(url, headers=headers, timeout=3)
        #print(content)

        jsondata = content.json()
        mid2info = {}
        context = {}
        for k,v in jsondata.items():
            if k == "context":
                context = v
            elif k.isdigit():
                mid = v["mid"]
                mid2info[mid] = v
            else:
                pass

        return mid2info, context, jsondata

    def tab_recall(self, uid, page=1):
        '''
        调用Tab流的召回
        :param uid:
        :param page:
        :return:
        '''
        extension = '{"refresh_count":2}'
        extension = urllib.parse.quote(extension)
        domain = "http://10.182.9.194:6006/demo_yiqikan?"
        #domain = "http://interface.video.recom.weibo.com:6006/demo_yiqikan?"
        url = domain + "pid=827&containerid=231643_11_5009&uid={0}&page={1}&extension={2}&source=3439264077".format(uid, page, extension)
        print(url)
        headers = {}
        content = requests.get(url, headers=headers, timeout=3)
        jsondata = content.json()
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

    def white_recall(self, smid, uid, count=10, page=1, debug=False):
        '''
        调用White的召回
        :param smid: 导流mid
        :param uid:
        :param page:
        :return:
        # '''
        url = "http://10.85.132.217:9006/demo_wls?pid=823&source=3061639762&scene=feed&" \
              "uid={0}&count={3}&page={1}&mid={2}".format(uid, page, smid, count)

        if debug:
            print(url)

        headers = {}
        content = requests.get(url, headers=headers, timeout=3)
        jsondata = content.json()
        mid2info = {}
        context = {}
        cand = jsondata.get("cand", [])
        for item in cand:
            mid = item["mid"]
            feature = item.get("feature", {})
            mid2info[mid] = feature
            if debug:
                print("recall: %s %s" % (mid, json.dumps(feature)))

        ctx = jsondata.get("context", {})
        context["globalfeas"] = {}
        for item in ctx.get("feat", []):
            context["globalfeas"][item["fid"]] = item["val"]
        context["sessid"] = jsondata.get("sessid", "")
        context["bid"] = jsondata.get("bid", "")
        context["service"] = jsondata.get("service", "")
        context["model"] = jsondata.get("model", "")

        return mid2info, context, jsondata

if __name__ == "__main__":
    client = RecallClient()
    mid2info, context, content = client.black_recall("4439295278065207", "2201423134")
    print(context)
    print(len(mid2info))
