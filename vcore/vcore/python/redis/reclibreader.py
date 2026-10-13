# _*_ coding: utf-8 _*_
# @Time    : 2019/9/29 3:34 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : reclibreader.py
#
# redis可推荐库的reader类
#
# 数据的存储格式为zset，其中
# key格式为小时存储格式，如’2019091321’(即存储为2019091321发布的mid数据)，
# value为mid，score为融合清晰度和ace分值先验分值  by @王雷

import redis
from datetime import datetime, timedelta
from vcore.python.utils.redisproxy import RedisProxy
from vcore.python.utils.midtool import MidTool

class ReclibReader(object):

    def __init__(self, addr, redisproxy = None):
        '''
        :param addr: 格式如 ("rm51826.eos.grid.sina.com.cn", 51826, 3)
        :param redisproxy
        '''
        if not redisproxy:
            self.redisproxy = RedisProxy()
        else:
            self.redisproxy = redisproxy
        self.key = "reclib"
        addrlist = []
        addrlist.append(addr)
        self.redisproxy.new_pool_list(self.key, addrlist, 5, 2, 2)

        self.date_format = "%Y%m%d%H"

    def get_mids(self, start_ts, end_ts):
        '''
        读取可推荐库里面的mid
        :param start_ts:
        :param end_ts:
        :return: {mid1:score, mid2:score, ....}
        '''
        keys = self.get_ts_keys(start_ts, end_ts)
        if not keys:
            return {}

        mid2score = {}
        conn = self.redisproxy.get_rand_connection(self.key)
        tmp_keys = []
        for dt_key in keys:
            tmp_keys.append(dt_key)
            if len(tmp_keys) >= 5:
                pipe = conn.pipeline(transaction=False)
                for key in tmp_keys:
                    pipe.zrange(key, 0, -1, withscores=True)
                result = pipe.execute()
                for midlist in result:
                    for mid, score in midlist:
                        mid2score[mid] = score

                tmp_keys.clear()

        if tmp_keys:
            pipe = conn.pipeline(transaction=False)
            for key in tmp_keys:
                pipe.zrange(key, 0, -1, withscores=True)
            result = pipe.execute()
            for midlist in result:
                for mid, score in midlist:
                    mid2score[mid] = score

        return mid2score

    def get_ts_keys(self, start_ts, end_ts):
        '''
        获取一个时间范围内的所有redis key
        :param start_ts: 起始时间戳
        :param end_ts:  终止时间戳
        :return: [key1, key2, ....]
        https://stackoverflow.com/questions/44683774/have-a-list-of-hours-between-two-dates-in-python
        '''
        start_dt = datetime.fromtimestamp(int(start_ts))
        end_dt = datetime.fromtimestamp(int(end_ts))
        assert start_dt < end_dt
        keys = []
        while start_dt <= end_dt:
            keys.append(start_dt.strftime(self.date_format))
            start_dt += timedelta(hours=1)
        return keys

    def check_mid(self, target_mid):
        '''
        检查mid是否在可推库
        :param mid:
        :return:
        '''
        ts = MidTool.get_ts(target_mid)
        dt = datetime.fromtimestamp(int(ts))
        dtkey = dt.strftime(self.date_format)
        conn = self.redisproxy.get_rand_connection(self.key)
        midlist = conn.zrange(dtkey, 0, -1, withscores=True)
        print("mid num: ", len(midlist))
        for mid, score in midlist:
            if str(mid) == target_mid:
                return True
        return False

