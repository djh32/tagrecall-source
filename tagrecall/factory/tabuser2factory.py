# _*_ coding: utf-8 _*_
# @Time    : 2019/11/28 5:22 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabuserfactory.py
# tab流的同作者召回，时间序

import logging
import zlib
import json
from .recallfactory import RecallFactory
from vcore.python.utils.midtool import MidTool

class TabUser2Factory(RecallFactory):

    def __init__(self, **kwargs):
        super(TabUser2Factory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        uid = str(minfo.get("100307", ""))
        if uid:
            return [(uid, {})]
        return []

    def rank(self, stream_name, stream, mid2info):
        '''
        排序函数: 默认取全局排序的score
        :param stream:
        :param mid2info:
        :return:
        '''
        for mid, detail in stream.midlist:
            score = MidTool.get_ts(mid)
            stream.midwithscore.append((mid, score))
        stream.midwithscore = sorted(stream.midwithscore, reverse=True, key=lambda x: x[1])

    def format(self, stream_name, stream, mid2info):
        '''
        格式化要写入redis的数据
        :param stream_name:
        :param stream:
        :param mid2info:
        :return:
        '''
        content = []
        for mid, score in stream.midwithscore:
            uid = mid2info[mid].get("100307", "")
            vert = mid2info[mid].get("10566", "0")
            gid = mid2info[mid].get("10988", "0")
            if not uid:
                continue
            cand_info = {"mid": str(mid), "aid": str(uid), "score": str(round(score, 4)), "vert": int(vert)}
            if gid != "0":
                cand_info["gid"] = str(gid)
            content.append(cand_info)

        if not content:
            return ""
        content = zlib.compress(json.dumps(content).encode("ascii"))
        return content

