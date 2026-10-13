# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 4:18 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : nonefilter.py
# 不存在过滤器，特征不存在或者为空则过滤

from .filter import Filter, del_count

class NoneFilter(Filter):

    def __init__(self, name, *args, **kwargs):
        super(NoneFilter, self).__init__(name, *args, **kwargs)
        # 特征名称
        self.fid = kwargs["fid"]

    @del_count
    def check(self, mid, midinfo):
        if self.fid not in midinfo or not midinfo[self.fid] or midinfo[self.fid] == "NULL":
            #print(self.name, " ", mid)
            return False
        return True