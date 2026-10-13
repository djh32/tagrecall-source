# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 4:18 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : lesscountfilter.py
# 计数器过滤器，小于某个值则过滤

from .filter import Filter, del_count

class LessCountFilter(Filter):

    def __init__(self, name, *args, **kwargs):
        super(LessCountFilter, self).__init__(name, *args, **kwargs)
        # 特征名称
        self.fid = kwargs["fid"]
        # 计数的阈值
        self.threshold = float(kwargs["threshold"])
        # 如果特征不存在的默认值
        self.default = float(kwargs["default"])

    @del_count
    def check(self, mid, midinfo):
        val = midinfo.get(self.fid, self.default)
        if val < self.threshold:
            return False
        return True