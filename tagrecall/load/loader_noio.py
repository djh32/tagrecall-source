# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 3:47 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : loader_noio.py
# 不需要读取IO，特征从已有数据提取

import logging
import time
from datetime import datetime
from collections import defaultdict
from .loader import Loader
from vcore.python.utils.midtool import MidTool

class NoioLoader(Loader):

    def __init__(self, **kwargs):
        super(NoioLoader, self).__init__(**kwargs)
        self.counter = defaultdict(int)

    def reset(self):
        self.counter.clear()

    def load(self, midlist, mid2info):
        for mid in midlist:
            if mid not in mid2info:
                mid2info[mid] = {}
            # mid的发布时间
            mid2info[mid]["ts"] = MidTool.get_ts(mid)

    def print_log(self):
        logging.info("******* no-io loader info {} *********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))