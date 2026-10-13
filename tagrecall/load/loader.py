# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 3:00 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : loader.py
# 加载各种特征

import importlib

def new_loader(class_name, params):
    '''
    根据类名反射生成一个
    :param class_name:
    :return:
    '''
    tmp_name = class_name.lower()
    module_name = "loader_" + tmp_name.replace("loader", "")
    module = importlib.import_module(".{}".format(module_name), __package__)
    loaderclass = getattr(module, class_name)
    return loaderclass(**params)

class Loader(object):

    def __init__(self, **kwargs):
        pass

    def load(self, midlist, mid2info):
        '''
        加载midlist中每个mid的各种特征
        特征会被写入到mid2info中
        :return: None
        '''
        pass

    def print_log(self):
        pass