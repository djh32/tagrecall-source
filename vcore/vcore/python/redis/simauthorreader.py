# _*_ coding: utf-8 _*_
# @Time    : 2020/7/22 8:27 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : simauthorreader.py
# 相似作者reader

import redis
import json
from vcore.python.utils.redisproxy import RedisProxy

class SimAuthorReader(object):

    def __init__(self):
        self.redisproxy = RedisProxy()
        self.key = "simauthor"
        addr = ("rm23519.mars.grid.sina.com.cn", 23519, 0)
        addrlist = []
        addrlist.append(addr)
        self.redisproxy.new_pool_list(self.key, addrlist, 5, 2, 2)

    def load_sim2authors(self, author_set):
        '''
        返回的数据和从redis里面拿到的是反的
        '''
        sim2authors = {}
        conn = self.redisproxy.get_rand_connection(self.key)
        tmp = []
        for aid in author_set:
            tmp.append(aid)
            if len(tmp) >= 2:
                pipe = conn.pipeline(transaction=False)
                for tmp_aid in tmp:
                    pipe.get(tmp_aid)
                result = pipe.execute()
                for idx, sim_str in enumerate(result):
                    if not sim_str:
                        continue
                    author = tmp[idx]
                    sim_str = sim_str.replace("\'", "\"")
                   #print(sim_str)
                    sim_info = json.loads(sim_str)
                    for info in sim_info:
                        sim_uid = info["simuid"]
                        score = info["score"]
                        if sim_uid not in sim2authors:
                            sim2authors[sim_uid] = []
                        sim2authors[sim_uid].append((author, score))
                tmp.clear()

        if tmp:
            pipe = conn.pipeline(transaction=False)
            for tmp_aid in tmp:
                pipe.get(tmp_aid)
            result = pipe.execute()
            for idx, sim_str in enumerate(result):
                if not sim_str:
                    continue
                author = tmp[idx]
                sim_str = sim_str.replace("\'", "\"")
                #print(sim_str)
                sim_info = json.loads(sim_str)
                for info in sim_info:
                    sim_uid = info["simuid"]
                    score = info["score"]
                    if sim_uid not in sim2authors:
                        sim2authors[sim_uid] = []
                    sim2authors[sim_uid].append((author, score))
            tmp.clear()

        return sim2authors



