# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 10:49 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabtagfactory.py

import zlib
import json
from tagrecall.factory.recallfactory import RecallFactory
from tagrecall.utils.tools import parse_wbtag

MANULE = "manule"
MACHINE = "machine"


class TabTagFactory(RecallFactory):

    def __init__(self, **kwargs):
        super(TabTagFactory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        '''
            判断一个mid应该放到哪些流里面
            一个mid可以放到多个recall-stream里面
            返回的streaminfo: (name, detail)
        '''
        (l1str, l1_type) = self._merge_tag(minfo, "10482", "10419")
        (l2str, l2_type) = self._merge_tag(minfo, "10483", "10420")
        (l3str, l3_type) = self._merge_tag(minfo, "10484", "10421")
        ret = []
        tagset = set()
        self._parse_tag(ret, tagset, l1str, l1_type, 0.8)
        self._parse_tag(ret, tagset, l2str, l2_type, 0.8)
        self._parse_tag(ret, tagset, l3str, l3_type, 0.7)

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
            cand_info = {"mid": str(mid), "aid": str(uid), "score": str(round(score, 4)), "tg_ty": ttype}
            if gid != "0":
                cand_info["gid"] = str(gid)
            content.append(cand_info)
        if not content:
            return ""
        content = zlib.compress(json.dumps(content).encode("ascii"))
        return content

    def _merge_tag(self, minfo, manual_tag_fid, machine_tag_fid):
        """
        优先人工标签
        :return: (tagstr, fid)，返回fid，用于后续
        """
        tagstr = minfo.get(manual_tag_fid, "")
        tag_type = MANULE
        if not tagstr:
            tagstr = minfo.get(machine_tag_fid, "")
            tag_type = MACHINE
        return (tagstr, tag_type)

    def _parse_tag(self, result, tagset, tagstr, tag_type, threshold):
        """
        :param result:
        :param tagset:
        :param tagstr:
        :param fid_type: 对fid_type是 机器类型的，实时threshold规则，人工的不适用该规则
        :param threshold:
        :return:
        """
        taglist = parse_wbtag(tagstr)
        for tagid, weight in taglist:
            # 只对机器标签实施 threshold 规则
            if tag_type == MACHINE and float(weight) < threshold:
                continue
            if tagid in tagset:
                continue
            result.append((str(tagid), {"w": weight}))
            tagset.add(tagid)