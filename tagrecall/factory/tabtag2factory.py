# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 10:49 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabtagfactory.py

import zlib
import json
from tagrecall.factory.recallfactory import RecallFactory
from tagrecall.utils.tools import parse_wbtag
from tagrecall.utils.tools import parse_tougao_tag

class TabTag2Factory(RecallFactory):

    def __init__(self, **kwargs):
        super(TabTag2Factory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        '''
            判断一个mid应该放到哪些流里面
            一个mid可以放到多个recall-stream里面
            返回的streaminfo: (name, detail)
        '''
        c1str = minfo.get("10748", "")
        c2str = minfo.get("10749", "")
        c3str = minfo.get("10750", "")
        ret = []
        c1tags = parse_tougao_tag(c1str)
        for tagid in c1tags:
            ret.append((str(tagid), {}))
        c2tags = parse_tougao_tag(c2str)
        for tagid in c2tags:
            ret.append((str(tagid), {}))
        c3tags = parse_tougao_tag(c3str)
        for tagid in c3tags:
            ret.append((str(tagid), {}))

        return ret

    def format(self, stream_name, stream, mid2info):
        '''
        格式化要写入redis的数据
        :param stream_name:
        :param stream:
        :param mid2info:
        :return:
        '''
        content = []
        ttype = "l3"
        if stream_name.startswith("1042015:newTagCategory"):
            ttype = "l1"
        elif stream_name.startswith("1042015:newAbilityTag"):
            ttype = "l2"

        for mid, score in stream.midwithscore:
            uid = mid2info[mid].get("100307", "")
            gid = mid2info[mid].get("10988", "0")
            if not uid:
                continue
            cand_info = {"mid":str(mid), "aid":str(uid), "score":str(round(score, 4)), "tg_ty":ttype}
            if gid != "0":
                cand_info["gid"] = str(gid)
            content.append(cand_info)
        if not content:
            return ""
        content = zlib.compress(json.dumps(content).encode("ascii"))
        return content
