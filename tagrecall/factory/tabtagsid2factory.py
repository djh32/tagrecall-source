# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 10:49 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabtagsidfactory.py
# 大数据标签

import zlib
import json
from tagrecall.factory.recallfactory import RecallFactory
from tagrecall.utils.tools import parse_wbtag


MANULE = "manule"
MACHINE = "machine"

class TabTagSid2Factory(RecallFactory):

    def __init__(self, **kwargs):
        super(TabTagSid2Factory, self).__init__(**kwargs)

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
        for mid, score in stream.midwithscore:
            oid = mid2info[mid].get("10650", "")
            uid = mid2info[mid].get("100307", "")
            if not oid or not uid:
                continue
            content.append({"mid":mid, "oid":oid, "aid":str(uid), "tg_sc":round(score, 4)})
        if not content:
            return ""
        content = zlib.compress(json.dumps(content).encode("ascii"))
        return content

    def after_rank(self, stream_name, stream, mid2info):
        '''
        排序后的处理。
        默认需要过滤相同的gid，oid，simhash，需要截断操作。
        :param stream:
        :param mid2info:
        :return:
        '''
        tmp = []
        gidset = set()
        oidset = set()
        shashset = set()
        for mid, score in stream.midwithscore:
            # oid = mid2info[mid].get("10650", "")
            # # 没有oid或者oid已出现
            # if not oid or oid in oidset:
            #     continue

            # 没有gid或者gid已出现
            gid = mid2info[mid].get("10988", "")
            if not gid or gid in gidset:
                continue

            # # 有sim-hash且sim-hash已出现 offline sim-hash
            # shash = mid2info[mid].get("simh", "")
            # if shash and shash in shashset:
            #     continue

            # 没有被过滤掉
            tmp.append((mid, score))
            # 教育标签要求物料多，教育类 L1 id换成 大数据 教育 id
            if "1042015:newTagCategory_039" in stream_name:
                if len(tmp) >= 3000:
                    break
            else:
                if len(tmp) >= self.num:
                    break
            gidset.add(gid)
            # oidset.add(oid)
            # shashset.add(shash)

        stream.midwithscore = tmp
        return

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
