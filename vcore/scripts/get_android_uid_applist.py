# _*_ coding: utf-8 _*_
# @Time    : 2020/7/17 10:03 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : get_android_uid_applist.py

import os
import sys
from collections import defaultdict
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from vcore.python.http.waicreader import WAICReader

def load_uids(file):
    uidset = set()
    inf = open(file)
    for line in inf:
        line = line.strip()
        if line != "":
            uidset.add(line)
    inf.close()
    return uidset

if __name__ == "__main__":

    uidset = load_uids("./android_uids.data")
    uidlist = list(uidset)
    print("total uid num: ", len(uidlist))
    fidlist = ["260002"]
    wreader = WAICReader()
    result = wreader.read_uid_feas(uidlist, fidlist)

    validn = 0
    app2count = defaultdict(int)
    for k,v in result.items():
        appstr = v.get("260002", "")
        if not appstr:
            continue
        validn += 1
        apps = appstr.split("|")
        for app in apps:
            kv = app.split("@")
            if len(kv) == 2:
                app = kv[0]
            app2count[app] += 1

    print("valid uid num: ", validn)
    print("#########################################")

    for k,v in app2count.items():
        print(k, "\t", v)