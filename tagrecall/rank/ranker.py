# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 10:25 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : ranker.py
import importlib

def new_ranker(class_name, params):
    '''
    根据类名反射生成一个
    :param class_name:
    :return:
    '''
    module_name = class_name.lower()
    module = importlib.import_module(".{}".format(module_name), __package__)
    rankerclass = getattr(module, class_name)
    return rankerclass(**params)

class Ranker(object):

    def __init__(self, **kwargs):
        pass

    def get_score(self, midinfo):
        pass