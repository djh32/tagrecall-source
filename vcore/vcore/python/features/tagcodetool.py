# _*_ coding: utf-8 _*_
# @Time    : 2019/10/30 4:01 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tagcodetool.py

from vcore.python.http.waicreader import WAICReader
from vcore.python.utils.redisproxy import RedisProxy

class TagcodeTool(object):

    def __init__(self):
        self.wreader = WAICReader()
        self.rproxy = RedisProxy()
        self.rproxy.new_pool_list("tagdb", [["rm51826.eos.grid.sina.com.cn", 51826, 14]])

    @staticmethod
    def get_ty(tagcode):
        '''
        根据我们的tagcode得到它是哪一类标签
        一级标签：0～999。大数据一级：0～99，投稿一级：100～199
        二级标签：1000～99999。大数据二级：1000～2999，投稿二级：3000～3999，topic：10000～99999
        关键词：100000~9999999。
        :param tagcode:
        :return:
        '''
        tagcode = int(tagcode)
        assert tagcode >= 0
        if tagcode <= 99:
            return "l1" # 大数据一级
        elif tagcode <= 199:
            return "c1" # 投稿一级
        elif tagcode <= 2999:
            return "l2" # 大数据二级
        elif tagcode <= 3999:
            return "c2" # 投稿二级
        elif tagcode <= 99999:
            return "tp" # topic
        else:
            return "kw" # keywords

    def get_tagid(self, tagcodelist):
        '''
        tagcode到tagid
        :param tagcode:
        :return:
        '''
        conn = self.rproxy.get_rand_connection("tagdb")
        pipe = conn.pipeline(transaction=False)
        keys = ["c2i_" + str(tagcode) for tagcode in tagcodelist]
        for key in keys:
            pipe.get(key)
        result = pipe.execute()
        return result

    def get_tagname(self, tagcodelist):
        '''
        tagcode到tagname的映射
        :param tagcode:
        :return:
        '''
        conn = self.rproxy.get_rand_connection("tagdb")
        pipe = conn.pipeline(transaction=False)
        keys = ["c2n_" + str(tagcode) for tagcode in tagcodelist]
        for key in keys:
            pipe.get(key)
        result = pipe.execute()
        return result

    def get_tagcode(self, tagidlist):
        '''
        tagid到tagcode的映射
        :param tagcode:
        :return:
        '''
        conn = self.rproxy.get_rand_connection("tagdb")
        pipe = conn.pipeline(transaction=False)
        keys = ["i2c_" + str(tagid) for tagid in tagidlist]
        for key in keys:
            pipe.get(key)
        result = pipe.execute()
        return result

    def get_wbtag_name(self, wbtaglist):
        '''
        微博标签ID到名称
        :param wbtaglist:
        :return: [tagname, tagname, ....]
        '''
        ret = self.wreader.read_obj_feas(wbtaglist, ["622"])
        names = [ret.get(tagid, {}).get("622", "") for tagid in wbtaglist]
        return names
