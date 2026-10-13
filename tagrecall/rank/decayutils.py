# _*_ coding: utf-8 _*_
# @Time    : 2019/7/21 11:16 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : decayutils.py
#
# 时间衰减

import datetime
import time
import math

FLOW = [
    ("0", 10285),
    ("1", 5801),
    ("2", 3560),
    ("3", 3974),
    ("4", 3177),
    ("5", 3378),
    ("6", 4419),
    ("7", 7121),
    ("8", 9962),
    ("9", 10321),
    ("10", 10536),
    ("11", 10840),
    ("12", 12301),
    ("13", 11926),
    ("14", 12601),
    ("15", 14735),
    ("16", 14144),
    ("17", 13022),
    ("18", 13638),
    ("19", 13616),
    ("20", 14425),
    ("21", 16873),
    ("22", 18410),
    ("23", 15425),
]

class DecayUtils():

    def __init__(self):
        total = sum([count for hour, count in FLOW])
        self.normalized_hour = dict([(hour, count * 24.0 / total ) for hour, count in FLOW])

    def get_normalized_decay(self, ts, half_time = 24 * 3600):
        tmp = 0.6931471805599453
        half_time = half_time / tmp
        now = int(time.time())
        delta = self.get_normalized_hours(ts, now)
        if delta < 0:
            return 1
        delta *= 3600
        decay = math.exp(-(delta / float(half_time)))
        return decay

    def get_decay(self, ts, half_time = 24 * 3600):
        tmp = 0.6931471805599453
        half_time = half_time / tmp
        now = int(time.time())
        delta = now - ts
        if delta < 0:
            return 1
        decay = math.exp(-(delta / float(half_time)))
        return decay

    def get_decay_by_delta(self, delta, half_time = 24 * 3600):
        '''
        时间衰减函数
        :param delta:   衰减时间
        :param half_time: 半衰期
        :return:
        '''
        tmp = 0.6931471805599453
        half_time = half_time / tmp
        if delta < 0:
            return 1
        decay = math.exp(-(delta / float(half_time)))
        return decay

    '''
     获取按照流量归一化后的时间间隔（小时级）
    '''
    def get_normalized_hours(self, startts, endts):
        hours = self.get_hours(endts, startts)
        ret = 0
        for h in hours:
            ret += self.normalized_hour[h]
        return ret

    '''
     获取startts到endts历经的小时
    '''
    def get_hours(self, endts, startts):
        ret = []
        assert endts >= startts
        startdt = datetime.datetime.fromtimestamp(startts)
        starthour = startdt.hour
        ret.append(str(starthour))

        hours = (endts - startts) // 3600
        hours = min(48, hours)
        for i in range(1, hours + 1):
            tmphour = (starthour + i) % 24
            ret.append(str(tmphour))
        return ret
        # for i in range(0, 48):
        #     nexthour = startdt + relativedelta.relativedelta(hours=i)
        #     hour = nexthour.hour
        #     ret.append(str(hour))
        #     tmpts = int(time.mktime(nexthour.timetuple()))
        #     if tmpts + 3600 >= endts:
        #         break
        # return ret

if __name__ == '__main__':
    startts = 1515342600
    endts = 1515441600
    utils = DecayUtils()
    ret = utils.get_hours(endts, startts)
    print(ret)
    ret = utils.get_normalized_hours(startts, endts)
    print(ret)

    endts = int(time.time())
    startts = endts - 12 * 3600
    print(utils.get_decay(endts - 24 * 3600, 7 * 24 * 3600))
    print(utils.get_decay(endts - 2 * 24 * 3600, 7 * 24 * 3600))
    print(utils.get_decay(endts - 3 * 24 * 3600, 7 * 24 * 3600))
    print(utils.get_decay(endts - 4 * 24 * 3600, 7 * 24 * 3600))
    print(utils.get_decay(endts - 5 * 24 * 3600, 7 * 24 * 3600))
    print(utils.get_decay(endts - 6 * 24 * 3600, 7 * 24 * 3600))
    print(utils.get_decay(endts - 7 * 24 * 3600, 7 * 24 * 3600))



