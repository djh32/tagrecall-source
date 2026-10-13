# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 2:35 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : creator.py

import importlib

def new_factory(params):
    cls_name = params["class"]
    module_name = cls_name.lower()
    module = importlib.import_module(".{0}".format(module_name), __package__)
    factory = getattr(module, cls_name)
    return factory(**params)