# _*_ coding: utf-8 _*_
# @Time    : 2019/10/18 8:18 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : run_default_worker.py

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import tagrecall.context
from tagrecall.worker.worker_redis_byKey import DefaultWorker
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("conf", type=str,
                        help="configure file")
    args = parser.parse_args()

    config_file = args.conf
    config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config/{}'.format(config_file)))
    if not os.path.isfile(config_file):
        raise Exception("{} does not exist.".format(config_file))

    worker = DefaultWorker(config_file)
    worker.run()