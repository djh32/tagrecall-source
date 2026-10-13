# _*_ coding: utf-8 _*_
# @Time    : 2019/9/2 6:22 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : openapis.py

import json
import requests
import traceback
from vcore.python.utils.tauth2proxy import TAuth2

class OpenApis():

    def __init__(self, name = "aliyun"):
        self.source = "981203697"
        self.authproxy = TAuth2(name, self.source)

    '''
    批量查询mid
    http://wiki.intra.weibo.com/1/statuses/show_batch
    return: {id1:{.....}, id2:{......}}
    '''
    def statuses_showbatch(self, ids,
                           trim_user=0, simplify="1,3,4,5,6,8", is_encoded=0, isGetLongText=1, timeout=1):
        url = "http://i.api.weibo.com/2/statuses/show_batch.json?" \
              "source={0}" \
              "&ids={1}" \
              "&trim_user={2}" \
              "&simplify={3}" \
              "&is_encoded={4}" \
              "&isGetLongText={5}".format(self.source, ids, trim_user, simplify, is_encoded, isGetLongText)

        content = self._http(url, self.source, timeout=timeout)
        if "statuses" not in content:
            return {}
        if not isinstance(content["statuses"], list):
            return {}
        idlist = ids.split(",")
        return dict(zip(idlist, content["statuses"]))

    '''
    批量查用户
    http://wiki.intra.weibo.com/1/users/show_batch
    return： {"uid1":{"id":uid1, "name":xxx, ...}, ....}
    '''
    def user_showbatch(self, uids, timeout=3):
        url = "http://i.api.weibo.com/users/show_batch.json?" \
            "uids={0}&" \
            "simplify=1,2,3,4,5,6,7,8&" \
            "trim_status=1".format(uids)
        content = self._http(url, self.source, timeout=timeout)
        if "users" not in content:
            return {}
        if not isinstance(content["users"], list):
            return {}
        ret = {}
        for user in content["users"]:
            ret[str(user["id"])] = user
        return ret

    def _http(self, url, uid, timeout=1):
        try:
            headers = {"Authorization": self.authproxy.get_token(uid), 'Connection': 'close'}
            content = requests.get(url, headers=headers, timeout=timeout)
            if "error_code" in content:
                raise Exception(str(uid) + ": " + json.dumps(content))
            return content.json()
        except:
            traceback.print_exc()
            return {}

