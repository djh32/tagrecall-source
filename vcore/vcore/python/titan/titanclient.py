# _*_ coding: utf-8 _*_
# @Time    : 2019/11/17 7:47 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : titan.py

import os
import time
import random
import grpc
import titan_pb2
import titan_pb2_grpc
import basic_pb2
#import vcore.python.titan.basic_pb2
import asyncio

class TitanClient():

    def __init__(self, host, port):
        channel = grpc.insecure_channel(str(host) + ":" + str(port))
        self.client = titan_pb2_grpc.TitanStub(channel)

    def midrank(self, bid, sessid, model, smid, uid, mid2feas, globalfeas, num, retfid = list(["recom_code"]), debug=True):
        cands = []
        for mid, feas in mid2feas.items():
            fl = basic_pb2.FeatList()
            fl.id = mid
            for fid, val in feas.items():
                f = fl.feat.add()
                f.fid = fid
                f.val = val.encode("utf-8")
            cands.append(fl)

        context = basic_pb2.FeatList()
        for fid, val in globalfeas.items():
            f = context.feat.add()
            f.fid = fid
            f.val = str(val).encode("utf-8")

        request = titan_pb2.MidRankRequest(
            bid=bid,
            sessid=sessid,
            model=model,
            smid=smid,
            uid=uid,
            cand=cands,
            context=context,
            num=num,
            debug=debug,
            retfid=retfid
        )

        response = self.client.MidRank(request)
        return response

    def uidrank(self, bid, sessid, model, uid, mid2feas, globalfeas, num, retfid = list(["recom_code"]), debug=True):
        cands = []
        for mid, feas in mid2feas.items():
            fl = basic_pb2.FeatList()
            fl.id = mid
            for fid, val in feas.items():
                f = fl.feat.add()
                f.fid = fid
                f.val = val.encode("utf-8")
            cands.append(fl)

        context = basic_pb2.FeatList()
        for fid, val in globalfeas.items():
            f = context.feat.add()
            f.fid = fid
            f.val = str(val).encode("utf-8")

        request = titan_pb2.UidRankRequest(
            bid=bid,
            sessid=sessid,
            model=model,
            uid=uid,
            cand=cands,
            context=context,
            num=num,
            debug=debug,
            retfid=retfid
        )

        response = self.client.UidRank(request)
        return response

    def uidrank2(self, bid, sessid, model, uid, mid2feas, globalfeas, num, retfid = list(["recom_code"]), debug=True):
        cands = []
        for mid, feas in mid2feas.items():
            fl = basic_pb2.FeatList()
            fl.id = mid
            for fid, val in feas.items():
                f = fl.feat.add()
                f.fid = fid
                f.val = val.encode("utf-8")
            cands.append(fl)

        context = basic_pb2.FeatList()
        for fid, val in globalfeas.items():
            f = context.feat.add()
            f.fid = fid
            f.val = str(val).encode("utf-8")

        request = titan_pb2.UidRankRequest(
            bid=bid,
            sessid=sessid,
            model=model,
            uid=uid,
            cand=cands,
            context=context,
            num=num,
            debug=debug,
            retfid=retfid
        )

        response = self.client.UidRank2(request)
        return response
    def recallFm(self,bid,uid,channel,version,globalfeas,num,debug=True):
        context = basic_pb2.FeatList()
        for fid, val in globalfeas.items():
            f = context.feat.add()
            f.fid = fid
            f.val = str(val).encode("utf-8")

        request = titan_pb2.RecallRequest(
            bid=bid,
            uid=uid,
            mid=uid,
            channel=channel,
            version=version,
            context=context,
            num=num,
            debug=debug
        )

        response = self.client.RecallFm(request)
        return response
