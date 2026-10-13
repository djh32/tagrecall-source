# _*_ coding: utf-8 _*_
# @Time    : 2019/9/27 3:46 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_waicapis.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from vcore.python.utils.waicapis import WAICApis

if __name__ == "__main__":
    apis = WAICApis()
    #result = apis.get_pid_features("005xpGjGly1g0yufeadjfj30u0140asa",
    #                                "1112,1150,1151")
    #print(result)

    mids = ",".join(["4420808971183357", "4420808363113606", "4420931201992994"])
    fids = ",".join(["10419", "10420"])
    result = apis.get_mid_features(mids, fids)
    print(result)