# _*_ coding: utf-8 _*_
# @Time    : 2019/12/11 5:16 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : hasfilter.py
# 有这个特征则物料被过滤

from .filter import Filter, del_count

class HasFilter(Filter):

    def __init__(self, name, *args, **kwargs):
        super(HasFilter, self).__init__(name, *args, **kwargs)
        # 特征名称
        self.fid = kwargs["fid"]

    @del_count
    def check(self, mid, midinfo):
        if self.fid in midinfo and midinfo[self.fid]:
            return False
        return True