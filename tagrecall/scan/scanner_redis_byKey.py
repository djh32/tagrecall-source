# _*_ coding: utf-8 _*_
# @Time    : 2021/1/26 5:10 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : scanner_mysql.py

import time
import logging
import redis
import json
from datetime import datetime
from collections import defaultdict
from .scanner import MidScanner


class MyRedisScanner(MidScanner):

    def __init__(self, host, port, db, table):
        """
        scan from redis
        :param host:
        :param port:
        :param db:
        :param table:
        """
        MidScanner.__init__(self)
        # table name is key name
        self.table = table
        self.rds = redis.Redis(host=host, port=int(port), db=int(db))
        self.counter = defaultdict(int)
        self.batch_n = 2000

    def get_mids(self, **kwargs):
        """
        从redis中获取运营投递的物料和信息
        [{'begin': '1637650800', # 开始时间
          'data_type': '1', # 1为置顶，0位不置顶
          'text': '明星父母实力',  # 流内推荐理由
          'mid': '4706430982818438',  # 投递物料 id
          'source': 'PCG_operation',  # 投递物料来源
          'aid': '6444928713',  # 作者id
          'is_all': '0',  # 1为全量用户洗发，0为非全量用户下发（兴趣匹配下发）
          'expired': '1637679600'   # 到期时间
        }]
        :param kwargs:
        :return: midlist,mid2info
        """
        st = time.time()
        midlist = []
        mid2info = {}

        results = json.loads(self.rds.get(self.table))
        for row in results:
            mid = str(row.get("mid", ""))
            if mid == "":
                break
            if mid in mid2info:
                continue
            midlist.append(mid)
            mid2info[mid] = row

        self.counter["cost"] = int(time.time() - st)
        self.counter["total"] = len(midlist)

        return midlist, mid2info

    def get_mids_test(self, **kwargs):
        pass

    def print_log(self):
        logging.info("******* reclib redis scanner info {} *********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("load cost time: {} seconds.".format(self.counter["cost"]))
        logging.info("total mid num: {}".format(self.counter["total"]))
