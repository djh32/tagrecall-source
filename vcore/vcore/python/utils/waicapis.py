# coding: utf-8
'''
调用WAIC平台获取特征
'''
import json
import requests
import traceback
from vcore.python.utils.tauth2proxy import TAuth2

class WAICApis():

    def __init__(self, name="aliyun"):
        self.source = "981203697"
        self.authproxy = TAuth2(name, self.source)

    def get_session(self):
        return requests.session()

    """
    根据uid，count, 获取用户关注的用户的 uid  
    """
    def get_friends_uids(self, uid, count = 50, cursor = -1):
        url = "http://i.api.weibo.com/2/friendships/friends/ids.json?uid={0}&count={1}&cursor={2}".format(uid, count, cursor)
        content = self._api(url, uid)
        return content

    '''
      获取mid特征
      http://waic.intra.weibo.com/#/console/dataplatform/dataapi/detail?datainfo_id=5
      多个mid，fid，uid都以逗号分割
    '''
    def get_mid_features(self, mids, fids, timeout=1, session=None):
        url = "http://i.feature.weibo.com/feature/mblog/query.json?source={2}&mids={0}&fids={1}".format(mids, fids, self.source)
        content = self._api(url, self.source, timeout=timeout, session=session)
        result = self._format_result(content)
        return result

    '''
      获取图像特征
      http://waic.intra.weibo.com/#/console/dataplatform/dataapi/detail?datainfo_id=66
    '''
    def get_pid_features(self, pids, fids, timeout=1):
        url = "http://i.feature.weibo.com/feature/picture/query.json?source={2}&pids={0}&fids={1}".format(pids, fids, self.source)
        content = self._api(url, self.source, timeout=timeout)
        return self._format_result(content)

    '''
      获取用户特征
      http://waic.intra.weibo.com/#/console/dataplatform/dataapi/detail?datainfo_id=3
      多个fid，uid都以逗号分割
    '''
    def get_user_features(self, uids, fids, timeout=1, session=None):
        url = "http://i.feature.weibo.com/feature/user/query.json?source={2}&uids={0}&fids={1}".format(uids, fids, self.source)
        content = self._api(url, self.source, timeout=timeout, session=session)
        result = self._format_result(content)
        return result

    '''
      获取对象特征
      http://waic.intra.weibo.com/#/console/manageplatform/document/markdown/detail?id=67
    '''
    def get_object_features(self, oids, fids, timeout=1):
        url = "http://i.feature.weibo.com/feature/object/query.json?source={2}&oids={0}&fids={1}".format(oids, fids, self.source)
        content = self._api(url, self.source, timeout=timeout)
        result = self._format_result(content)
        return result

    def _api(self, url, uid, timeout=1, session=None):
        try:
            headers = {"Authorization": self.authproxy.get_token(uid)}
            if session:
                content = session.get(url, headers=headers, timeout=timeout)
            else:
                content = requests.get(url, headers=headers, timeout=timeout)
            #print(content.json())
            if "error_code" in content:
                raise Exception(self.source + ": " + json.dumps(content))
            return content.json()
        except requests.ConnectTimeout as e:
            print("connect timetout")
            return {}
        except:
            traceback.print_exc()
            return {}

    def _format_result(self, json_result):
        if type(json_result) != dict:
            return {}
        if "data" not in json_result:
            return {}
        ret = json_result["data"]
        if type(ret) != dict:
            raise Exception(self.source + ": " + json.dumps(ret))
        return ret
