# _*_ coding: utf-8 _*_
# @Time    : 2019/10/22 4:27 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tagrecallreader.py
# 标签到midlist的reader

import zlib
import json
from vcore.python.utils.redisproxy import RedisProxy

class TagRecallReader(object):

    def __init__(self, host, port, db):
        self.proxy = RedisProxy()
        self.proxy.new_pool_list("topicdb", [[host, port, db, False]])

    def _get_conn(self):
        return self.proxy.get_rand_connection("topicdb")

    def get_tag_mids(self, tagid, prefix="", version=""):
        '''
        获得tagid对应的mids
        :param tagid:
        :return:  [{"mid":mid, "ty_sc":0},…]
        '''
        conn = self._get_conn()
        rkey = prefix + tagid + "_" + version if version else prefix + tagid
        content = conn.get(rkey)
        if not content:
            return []
        cstr = zlib.decompress(content)
        midlist = json.loads(cstr)
        return midlist