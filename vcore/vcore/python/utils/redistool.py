# _*_ coding: utf-8 _*_
# @Time    : 2019/9/29 10:44 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : redistool.py

import redis

class RedisTool(object):

    @staticmethod
    def new_conn(host, port, db=0,
                 socket_timeout=5,
                 socket_connect_timeout=5,
                 decode_responses=True):
        '''
        python3从redis里面读出的数据都是bytes
        但python2读出来的是string
        所以需要设置一下 decode_responses=True 这样保证redis读到的数据自动会被解析成utf-8的string
        如果存储的数据是二进制，则应该设置为False
        https://redis-py.readthedocs.io/en/latest/#redis.Connection
        https://stackoverflow.com/questions/44026515/python-redis-keys-returns-list-of-bytes-objects-instead-of-strings
        '''
        return redis.Redis(host=host, port=port, db=int(db),
                                    socket_timeout=socket_timeout,
                                    socket_connect_timeout=socket_connect_timeout,
                                    decode_responses=decode_responses)

    @staticmethod
    def new_localsocket_conn(socket_addr,
                 socket_timeout=5,
                 decode_responses=True):
        pool = RedisTool.new_localsocket_pool(socket_addr, 1, socket_timeout, decode_responses)
        return redis.Redis(connection_pool=pool)

    @staticmethod
    def get_conn(pool):
        return redis.Redis(connection_pool=pool)

    @staticmethod
    def new_pool(host, port, db=0,
                 conn_size=5,
                 socket_timeout=5,
                 socket_connect_timeout=5,
                 decode_responses=True):
        pool = redis.ConnectionPool(max_connections=conn_size,
                                    host=host, port=port, db=int(db),
                                    socket_timeout=socket_timeout,
                                    socket_connect_timeout=socket_connect_timeout,
                                    decode_responses=decode_responses)
        return pool

    @staticmethod
    def new_localsocket_pool(socket_addr,
                 conn_size=5,
                 socket_timeout=5,
                 decode_responses=True):
        pool = redis.ConnectionPool(connection_class=redis.UnixDomainSocketConnection,
                                    max_connections = conn_size,
                                    path=socket_addr,
                                    socket_timeout=socket_timeout,
                                    decode_responses=decode_responses)
        return pool