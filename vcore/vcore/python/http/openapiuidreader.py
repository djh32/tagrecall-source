# _*_ coding: utf-8 _*_
# @Time    : 2019/11/28 4:03 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : openapiuidreader.py

from datetime import datetime
from vcore.python.utils.openapis import OpenApis

class UidReader(object):

    def __init__(self, name = "aliyun"):
        self.apis = OpenApis(name)

    def get_users_basicinfo(self, uidlist, timeout=3):
        '''
        调用/users/show_batch接口
        :param uids:
        :return:
        '''
        batch = []
        content = {}
        for uid in uidlist:
            uid = str(uid)
            batch.append(uid)
            if len(batch) >= 40:
                uidstr = ",".join(batch)
                batch_ret = self.apis.user_showbatch(uidstr, timeout=timeout)
                content.update(batch_ret)
                batch = []

        if batch:
            uidstr = ",".join(batch)
            batch_ret = self.apis.user_showbatch(uidstr, timeout=timeout)
            content.update(batch_ret)

        ret = []
        for uid in uidlist:
            uid = str(uid)
            uidinfo = content.get(uid, {})
            uinfo = {"uid":uid}
            if uidinfo:
                uinfo["name"] = uidinfo.get("screen_name", "")
            ret.append(uinfo)
        return ret

