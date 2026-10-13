# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 4:48 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : loader_waic_mt.py
# 多线程读取waic特征的loader

import logging
import time
from datetime import datetime
from collections import defaultdict
from .loader import Loader
from vcore.python.http.waicreader import WAICReader
from vcore.python.features.fidconfig import MID_FID2NAME

# multi-thread-loader
class WaicMtLoader(Loader):

    def __init__(self, **kwargs):
        '''
        :param kwargs:
        @source_name:
        @fidlist: 特征列表
        @process_num: 进程数量
        '''
        super(WaicMtLoader, self).__init__(**kwargs)
        self.source_name = kwargs.get("source_name", "aliyun")
        self.reader = WAICReader(self.source_name)
        self.fidlist = kwargs.get("fidlist", [])
        self.process_num = int(kwargs.get("process_num", 10))

        self.counter = defaultdict(int)

    def reset(self):
        self.counter.clear()

    def set_fidlist(self, fidlist):
        '''
        设置要加载读取的特征
        :param fidlist:
        :return:
        '''
        self.fidlist = fidlist

    def load(self, midlist, mid2info):
        self.counter["total"] = len(midlist)
        start_ts = time.time()
        result = self.reader.mt_read_mid_feas(midlist, self.fidlist, self.process_num)
        end_ts = time.time()
        self.counter["cost"] = int(end_ts - start_ts)
        for ret in result:
            for mid, feas in ret.items():
                self.counter["valid"] += 1
                if mid in mid2info:
                    mid2info[mid].update(feas)
                else:
                    mid2info[mid] = feas
                for fid in feas:
                    if feas.get(fid, 0) == 0:
                        continue
                    self.counter[fid] += 1

    def print_log(self):
        logging.info("******* waic loader info {} *********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("load cost time: {} seconds.".format(self.counter["cost"]))
        logging.info("total mid num: {}".format(self.counter["total"]))
        logging.info("valid mid num: {0} {1}".format(self.counter["valid"], self.counter["valid"] / self.counter["total"]))
        fidn_list = list(self.counter.items())
        fidn_list = sorted(fidn_list, reverse=True, key=lambda x:x[1])
        for fid, num in fidn_list:
            if fid == "total" or fid == "valid" or fid == "cost":
                continue
            name = MID_FID2NAME.get(str(fid), "null")
            logging.info("fid {0}({1}) num: {2} {3}".format(fid, name, num, num / self.counter["valid"]))
