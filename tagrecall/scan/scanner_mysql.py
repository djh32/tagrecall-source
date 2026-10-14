# _*_ coding: utf-8 _*_
# @Time    : 2021/1/26 5:10 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : scanner_mysql.py

import time
import logging
import pymysql
from datetime import datetime
from collections import defaultdict
from .scanner import MidScanner

MYSQL_USER = "db_video_wbrec_r"
MYSQL_PWD = "4f7c415aeeb5a62"

class MysqlScanner(MidScanner):

    def __init__(self, host, port, db, table):
        MidScanner.__init__(self)
        self.table = table
        self.db = pymysql.connect(host = host,
                                  port = port,
                                  user = MYSQL_USER,
                                  password = MYSQL_PWD,
                                  database = db)
        self.cursor = self.db.cursor()
        self.counter = defaultdict(int)
        self.batch_n = 2000

    def reset(self):
        self.counter.clear()
        self.cursor = self.db.cursor()

    def get_mids(self, **kwargs):
        st = time.time()
        midlist = []
        mid2info = {}
        start_id = 0
        while True:
            # 扫描时把物料的 status/created_at/expired_at/updated_at 一并取出，
            # 用于后续排查「无 uid 物料是否因过期/下线导致」
            sql = "select id, status, created_at, expired_at, updated_at from {} where id > {} order by id limit {}".format(self.table, start_id, self.batch_n)
            # print(sql)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if not result:
                break
            for row in result:
                mid = row[0]
                if mid > start_id:
                    start_id = mid
                mid = str(mid)
                if mid in mid2info:
                    continue
                midlist.append(mid)
                mid2info[mid] = {
                    "status": row[1],
                    "created_at": str(row[2]) if row[2] is not None else "",
                    "expired_at": str(row[3]) if row[3] is not None else "",
                    "updated_at": str(row[4]) if row[4] is not None else "",
                }

        self.counter["cost"] = int(time.time() - st)
        self.counter["total"] = len(midlist)

        return midlist, mid2info

    def get_mids_test(self, **kwargs):
        start_id = 0
        batch_n = 100
        sql = "select id from {} where id > {} order by id limit {}".format(self.table, start_id, batch_n)
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for row in result:
            print(row[0])

    def print_log(self):
        logging.info("******* reclib redis scanner info {} *********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("load cost time: {} seconds.".format(self.counter["cost"]))
        logging.info("total mid num: {}".format(self.counter["total"]))
