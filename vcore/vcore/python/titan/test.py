# _*_ coding: utf-8 _*_
# @Time    : 2019/11/18 3:13 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : test.py

import os
import time
import random
import grpc
import titan_pb2
import titan_pb2_grpc
import basic_pb2

if __name__ == "__main__":

    print("hello world")

    channel = grpc.insecure_channel(str("10.85.132.234") + ":" + str(5100))
    client = titan_pb2_grpc.TitanStub(channel)