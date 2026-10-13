# _*_ coding: utf-8 _*_
# @Time    : 2019/8/26 8:18 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tauth2proxy.py

import hashlib
import hmac
import urllib.request, urllib.parse, urllib.error
import redis
import time
import base64

def hmacSignature(tauth_token_secret, param_str):
    h = hmac.new(tauth_token_secret,
                param_str.encode(), hashlib.sha1)
    s = h.digest()
    s = base64.b64encode(s)
    return str(s, "ascii").strip()

class TAuth2(object):

    def __init__(self, name = "aliyun", app_key="981203697"):
        self.app_key = app_key
        self.name = name
        self.tauth2_token = None
        self.tauth2_token_secret = None
        self.token_key = 'TOKEN_' + self.app_key + '_' + self.name + '_token'
        self.sign_key = 'TOKEN_' + self.app_key + '_' + self.name + '_secret'
        self.redis = None
        self.lastts = 0

        self.fetch_tauth_token()

    def fetch_tauth_token(self):
        mget_key = [self.token_key, self.sign_key]
        try:
            db = redis.Redis(host="rs20605.hebe.grid.sina.com.cn", port=20605, db=0)
            token_result = db.mget(mget_key)
            self.tauth2_token = token_result[0]
            self.tauth2_token_secret = token_result[1]
            self.lastts = int(time.time())
        except Exception as e:
            db = redis.Redis(host="rs20605.hebe.grid.sina.com.cn", port=20605, db=0)
            token_result = db.mget(mget_key)
            self.tauth2_token = token_result[0]
            self.tauth2_token_secret = token_result[1]
            self.lastts = int(time.time())

    def calc_auth_header(self, param):
        if not self.tauth2_token or not self.tauth2_token_secret:
            return ''
        sign = hmacSignature(self.tauth2_token_secret, param)
        m = {'token': self.tauth2_token, 'param': param, 'sign': sign}
        arr = urllib.parse.urlencode(m).split('&')
        authorizationHeader = "TAuth2 "
        for value in arr:
            pair = value.split("=")
            authorizationHeader += pair[0] + "=\"" + pair[1] + "\","
        return authorizationHeader[0:-1]

    def get_token(self, uid, clean_cache=False):
        if clean_cache or int(time.time()) - self.lastts > 120:
            self.fetch_tauth_token()
        # Calc tauth2 token for every param
        return self.calc_auth_header('uid=%s' % uid)

if __name__ == '__main__':
    ta2 = TAuth2()
    print(ta2.get_token("2085241395"))
