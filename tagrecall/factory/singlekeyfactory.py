# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 10:49 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : singlekeyfactory.py

import zlib
import json
import time
from tagrecall.factory.recallfactory import RecallFactory
from tagrecall.utils.tools import parse_wbtag

MANULE = "manule"
MACHINE = "machine"

class SingleKeyFactory(RecallFactory):
    def __init__(self, **kwargs):
        super(SingleKeyFactory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        """
        判断一个mid应该放到哪些流里面
        一个mid可以放到多个recall-stream里面
        返回的streaminfo: (name, detail)
        """
        (l1str, l1_type) = self._merge_tag(minfo, "10482", "10419")
        ret = []
        tagset = set()
        self._parse_tag(ret, tagset, l1str, l1_type, 0.8)
        return ret

    def format(self, stream_name, stream, mid2info):
        """
        :param stream_name:
        :param stream:
        :param mid2info:
        :return:
        """
        content = []

        for mid, score in stream.midwithscore:
            uid = mid2info[mid].get("100307", "")
            gid = mid2info[mid].get("10988", "0")
            if not uid:
                continue
            cand_info = {"mid": str(mid), "aid": str(uid), "score": str(round(score, 4))}
            if gid != "0":
                cand_info["gid"] = str(gid)
            content.append(cand_info)
        if not content:
            return ""
        # content = zlib.compress(json.dumps(content).encode("ascii"))
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
