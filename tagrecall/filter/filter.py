# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 3:11 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : filter.py

import functools

def del_count(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        result = func(self, *args, **kw)
        if not result:
            self.delcnt += 1
        return result

    return wrapper

class Filter(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        # 统计过滤调的mid个数
        self.delcnt = 0

    def reset(self):
        self.delcnt = 0

    @del_count
    def check(self, mid, midinfo):
        '''
        检查是否过滤
        :param mid:
        :param midinfo:
        :return: True: 不过滤 False：过滤
        '''
        return True