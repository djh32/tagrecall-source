# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 1:54 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tools.py

def parse_wbtag(tagstr):
    '''
    解析微博标签的字符串
    :param tagstr:
    :return:
    '''
    if not tagstr:
        return []
    items = tagstr.split("|")
    ret = []
    for item in items:
        kv = item.split("@")
        if len(kv) < 2:
            continue
        try:
            ret.append((kv[0], float(kv[1])))
        except Exception as e:
            print("Error for %s: %s" % (item, e))
    return ret

def parse_tougao_tag(tagstr):
    '''
    解析投稿标签（tagcode）
    :param tagstr:
    :return:
    '''
    if not tagstr:
        return []
    return tagstr.split("|")