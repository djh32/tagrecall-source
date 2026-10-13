# _*_ coding: utf-8 _*_
# @Time    : 2019/11/21 2:18 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabranker.py
# Tab流的默认排序公式

import time
from .ranker import Ranker
from .decayutils import DecayUtils

DECAY = DecayUtils()

class TabRanker(Ranker):

    def __init__(self, **kwargs):
        super(TabRanker, self).__init__(**kwargs)
        self.half_time = 20 * 24 * 3600
        self.alpha = 5.0
        self.beta = 20.0

    def get_score(self, midinfo):
        impn7day = int(midinfo.get("10776", 0))
        clkn7day = int(midinfo.get("10777", 0))
        impn24h = int(midinfo.get("10698", 0))
        clkn24h = int(midinfo.get("10700", 0))

        if impn24h > 50:
            ctr = clkn24h * 1.0 / impn24h
        elif impn7day > 50:
            ctr = clkn7day * 1.0 / impn7day
        else:
            ctr = (clkn7day + self.alpha) / (impn7day + self.beta)

        ctr_final = ctr

        # 时间衰减
        ts = midinfo.get("ts", 0)
        current = int(time.time())
        decay = self.time_decay(current - ts)
        return ctr_final * decay

    def time_decay(self, delta):
        '''
        7天半衰期
        :param delta:
        :return:
        '''
        return DECAY.get_decay_by_delta(delta, self.half_time)