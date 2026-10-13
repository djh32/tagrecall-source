# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 10:49 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabtagsidfactory.py
# 投稿ID（原始ID，非统一标签ID）的倒排

import zlib
import json
from tagrecall.factory.recallfactory import RecallFactory
from tagrecall.utils.tools import parse_tougao_tag

class TabTagSidFactory(RecallFactory):

    def __init__(self, **kwargs):
        super(TabTagSidFactory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        '''
            判断一个mid应该放到哪些流里面
            一个mid可以放到多个recall-stream里面
            返回的streaminfo: (name, detail)
        '''
        c1str = minfo.get("10588", "")
        c2str = minfo.get("10589", "")
        c3str = minfo.get("10590", "")
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
            # 教育标签要求物料多
            if "4379161553210523" in stream_name:
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
