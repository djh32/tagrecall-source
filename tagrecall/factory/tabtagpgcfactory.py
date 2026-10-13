# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 10:49 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabtagpgcfactory.py
# facfory: tab流内，pgc运营物料投递倒排工厂

import zlib
import json
import time
from tagrecall.factory.recallfactory import RecallFactory
from tagrecall.utils.tools import parse_wbtag

MANULE = "manule"
MACHINE = "machine"


class TabTagPgcFactory(RecallFactory):
    def __init__(self, **kwargs):
        super(TabTagPgcFactory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        """
        判断一个mid应该放到哪些流里面
        一个mid可以放到多个recall-stream里面
        如果 mid 全量下发（is_all = "1"）, 不再加入到l1/l2标签倒排中
        返回的streaminfo: (name, detail)
        """
        ret = []

        # 如果 is_all == 1, 该 mid 增加 is_all_1的召回流, 且不再增加到其他 l1/l2倒排中
        is_all = minfo.get("is_all", "0")
        if str(is_all) == "1":
            ret.append(("is_all_1", {}))
            return ret

        (l1str, l1_type) = self._merge_tag(minfo, "10482", "10419")
        (l2str, l2_type) = self._merge_tag(minfo, "10483", "10420")
        tagset = set()

        self._parse_tag(ret, tagset, l1str, l1_type, 0.8)
        self._parse_tag(ret, tagset, l2str, l2_type, 0.8)

        return ret

    def rank(self, stream_name, stream, mid2info):
        '''
        排序函数: 默认取全局排序的score
        按照 begin time 排序，先生效的排序在前面
        :param stream:
        :param mid2info:
        :return:
        '''
        for mid, detail in stream.midlist:
            score = float(mid2info[mid].get("begin", 0))
            stream.midwithscore.append((mid, score))
        stream.midwithscore = sorted(stream.midwithscore, reverse=False, key=lambda x: x[1])

    def format(self, stream_name, stream, mid2info):
        """
        :param stream_name:
        :param stream:
        :param mid2info:
        :return:
        """
        content = []
        ttype = "l2"
        if stream_name.startswith("1042015:newTagCategory"):
            ttype = "l1"
        elif stream_name.startswith("1042015:newAbilityTag"):
            ttype = "l2"
        elif stream_name == "is_all_1":
            ttype = "is_all_1"

        for mid, score in stream.midwithscore:
            uid = mid2info[mid].get("aid", "")
            gid = mid2info[mid].get("10988", "0")
            begin = mid2info[mid].get("begin", "")
            expired = mid2info[mid].get("expired", "")
            text = mid2info[mid].get("text", "")
            data_type = mid2info[mid].get("data_type", "0")
            is_all = mid2info[mid].get("is_all", "0")
            source = mid2info[mid].get("source", "")
            tg_ty = ttype

            if not uid:
                continue
            cand_info = {"mid": str(mid), "aid": str(uid), "score": str(round(score, 2)),
                         "begin": begin, "expired": expired, "text": text,
                         "data_type": data_type, "is_all": is_all, "source": source, "tg_ty": tg_ty}
            if gid != "0":
                cand_info.update({"gid": str(gid)})
            content.append(cand_info)
        if not content:
            return ""
        return content

    def write(self, mid2info):
        """
        1. 写入一个key的value内，tag2mids
        2. single key，不需要 redis pipe
        :param mid2info:
        :return:
        """
        # 所有stream写 singleKey_values
        conn = self.rproxy.get_rand_connection("writer")
        pipe = conn.pipeline(transaction=False)
        count = 0

        rkey = self.prefix + self.version
        rdata = {}
        for stream_name, stream in self.streams.items():
            mids = self.format(stream_name, stream, mid2info)
            if not mids:
                continue
            rdata.update({stream_name: mids})
        rdata = zlib.compress(json.dumps(rdata).encode("ascii"))

        # 写入 signle key and value
        pipe.set(rkey, rdata, ex=self.expire_time)
        self.counter["stream_num"] += 1
        pipe.execute()

        # 增加监控 eg: newtab_uid_v1_update
        alert_key = self.prefix + self.version + "_update"
        alert_data = int(time.time())
        pipe.set(alert_key, alert_data, ex=self.expire_time)
        pipe.execute()

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
