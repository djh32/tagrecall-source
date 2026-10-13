# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 7:48 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : cachefile.py

import json
import os
import logging
import time
from datetime import datetime

class CacheFile(object):

    def __init__(self):
        pass

    def write2file(self, filename, midlist, mid2info, mode="w"):
        filename = "%s_%s" % (filename, time.strftime("%Y%m%d"))
        filepath = self._filepath(filename)
        with open(filepath, mode, encoding="utf-8") as outf:
            for mid in midlist:
                outf.write(mid + "\t" + json.dumps(mid2info.get(mid, {})) + "\n")
        outf.close()

        logging.info("******* CacheFile write info {} *********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("write file: {}".format(filepath))
        logging.info("write mid number: {}".format(len(midlist)))

    def loadfile(self, filename):
        '''
        读取cache file
        :param filename:
        :return:  midlist 和 mid2info
        '''
        midlist = []
        mid2info = {}
        filepath = self._filepath(filename)
        with open(filepath, encoding="utf-8") as inf:
            for line in inf:
                items = line.split("\t", 1)
                if len(items) != 2:
                    continue
                info = json.loads(items[1])
                midlist.append(items[0])
                mid2info[items[0]] = info

        logging.info("******* CacheFile read info {} *********".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("read file: {}".format(filepath))
        logging.info("read mid number: {}".format(len(midlist)))

        return midlist, mid2info

    def _filepath(self, filename):
        '''
        cache文件都放到cache目录下
        :param filename:
        :return:
        '''
        return os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            '../../cache/{}'.format(filename)))