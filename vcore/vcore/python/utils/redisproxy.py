# _*_ coding: utf-8 _*_
# @Time    : 2019/9/29 10:26 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : redisproxy.py

import redis
import random
from .redistool import RedisTool

class RedisProxy():

    def __init__(self):
        self.pools = {}

    def new_pool_list(self, name, addrlist,
                 conn_size=5,
                 socket_timeout=5,
                 socket_connect_timeout=5):
        '''
        增加一个新的redis-connection-pool
        :param name:
        :param addrlist:
        :param conn_size:
        :param socket_timeout:
        :param socket_connect_timeout:
        :return:
        '''
        poollist = []
        for addr in addrlist:
            assert isinstance(addr, (list, tuple))
            # localsocket
            if len(addr) <= 2:
                socket_addr = addr[0]
                decode = addr[1] if len(addr) == 2 else True
                pool = RedisTool.new_localsocket_pool(socket_addr,
                                                      conn_size=conn_size,
                                                      socket_timeout=socket_timeout,
                                                      decode_responses=decode)
                poollist.append(pool)
            else:
                host = addr[0]
                port = addr[1]
                db = addr[2] if len(addr) >= 3 else 0
                decode = addr[3] if len(addr) >= 4 else True
                pool = RedisTool.new_pool(host, port, db=int(db),
                                            conn_size=conn_size,
                                            socket_timeout=socket_timeout,
                                            socket_connect_timeout=socket_connect_timeout,
                                            decode_responses=decode)
                poollist.append(pool)

        self.pools[name] = poollist

    def get_connection(self, key, idx):
        return redis.Redis(
            connection_pool=self.pools[key][idx])

    def get_rand_connection(self, key):
        pool = random.choice(self.pools[key])
        return redis.Redis(
            connection_pool=pool)

