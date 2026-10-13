# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 3:11 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : pipeline.py
# 过滤器的pipeline

from datetime import datetime
import logging
import json
from .filter import Filter
import importlib

def new_filter(name, class_name, params):
    '''
    根据配置文件的设置，通过反射初始化一个filter
    :param filter_name: e.g. "NoneFilter"
    :param params: e.g. {"fid":"10539"}
    :return:
    '''
    module_name = class_name.lower()
    module = importlib.import_module(".{}".format(module_name), __package__)
    filterclass = getattr(module, class_name)
    return filterclass(name, **params)

class Pipeline(object):

    def __init__(self):
        self.filters = []

    def add_filter(self, filter):
        '''
        添加新的filter
        :param filter:
        :return:
        '''
        self.filters.append(filter)

    def init_from_config(self, filter_config_list):
        if isinstance(filter_config_list, str):
            filter_config_list = filter_config_list.replace("\n", "")
            filter_config_list = json.loads(filter_config_list)
        '''
        根据一组配置初始化一个filter-list
        :param filter_config_list:
        :return:
        '''
        for config in filter_config_list:
            assert len(config) == 3
            name = config[0]
            class_name = config[1]
            params = config[2]
            assert isinstance(params, dict)
            f = new_filter(name, class_name, params)
            self.add_filter(f)

    def reset(self):
        '''
        过滤器的计数全部清零
        :return:
        '''
        for filter in self.filters:
            filter.reset()

    def check(self, midlist, mid2info):
        '''
        :param midlist:
        :param mid2info:
        :return: 返回过滤后的midlist
        '''
        ret = []
        for mid in midlist:
            info = mid2info.get(mid, {})
            status = True
            for filter in self.filters:
                status = filter.check(mid, info)
                if not status:
                    break

            if status:
                ret.append(mid)

        return ret

    def print_log(self):
        logging.info("******* filter statistic info {}*********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        for filter in self.filters:
            logging.info("{0} delete mid num: {1}".format(filter.name, filter.delcnt))