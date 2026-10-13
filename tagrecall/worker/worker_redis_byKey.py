# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 10:17 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : worker_redis_byKey.py

import time
import json
import logging
from configparser import ConfigParser
from datetime import datetime

from tagrecall.scan.scanner_redis_byKey import MyRedisScanner
from tagrecall.load.loader_waic_mt import WaicMtLoader
from tagrecall.load.loader import new_loader
from tagrecall.filter.pipeline import Pipeline
from tagrecall.factory.creator import new_factory
from tagrecall.rank.ranker import new_ranker
from .cachefile import CacheFile

class DefaultWorker(object):
    """
    default worker
    scan mid from redis by the key;
    key name from table
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(config_file, "UTF-8")

        # 读取物料库
        # host/port/db  is  redis address
        # table is the key of get redis
        host = self.config.get("Scan", "Host")
        port = self.config.get("Scan", "Port")
        db = self.config.get("Scan", "DB")
        table = self.config.get("Scan", "Table")
        self.scaner = MyRedisScanner(host, int(port), int(db), table)

        # 加载特征
        self.waicloader = WaicMtLoader(
            source_name=self.config.get("Load", "SourceName"),
            process_num=self.config.get("Load", "ProcessNumber"))

        # 默认排序ranker
        ranker_config = self.config.get("Rank", "DefaultRanker")
        ranker_config = json.loads(ranker_config)
        self.default_ranker = new_ranker(ranker_config[0], ranker_config[1])

        # 加载各种factory
        self.factories = []
        for section in self.config.sections():
            if section.startswith("Factory"):
                factory = new_factory(dict(self.config[section]))
                self.factories.append(factory)

    def run(self):
        logging.info("******************** default worker run {} *************************".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("config file: {}".format(self.config_file))

        midlist, mid2info = self.load_and_cache()
        logging.info("load mid num: {}".format(len(midlist)))

        loaders_config = self.config.get("Load", "OtherLoaderList")
        loaders_config = loaders_config.replace("\n", "")
        loaders_list = json.loads(loaders_config)
        for loader_name, params in loaders_list:
            assert isinstance(params, dict)
            newloader = new_loader(loader_name, params)
            newloader.load(midlist, mid2info)
            newloader.print_log()

        # 再做一遍基础过滤
        basicfilter_config = self.config.get("Filter", "BasicFilterList")
        basic_pipeline = Pipeline()
        basic_pipeline.init_from_config(basicfilter_config)
        midlist = basic_pipeline.check(midlist, mid2info)
        basic_pipeline.print_log()
        basic_pipeline.reset()

        # 计算默认的排序score
        for mid in midlist:
            minfo = mid2info[mid]
            default_score = self.default_ranker.get_score(minfo)
            minfo["default_score"] = default_score

        self.update(midlist, mid2info)

        logging.info("****** END. {} ******".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def update(self, midlist, mid2info):
        '''
        更新倒排索引
        :param midlist:
        :param mid2info:
        :return:
        '''
        for factory in self.factories:
            factory.handle(midlist, mid2info)
            factory.print_log()

    def load_and_cache(self):
        # 读取redis里面的可推荐库
        midlist, mid2info = self.scaner.get_mids()
        self.scaner.print_log()
        self.scaner.reset()

        # 加载特征
        sfids = json.loads(self.config.get("Load", "StaticFids"))
        dfids = json.loads(self.config.get("Load", "DynamicFids"))
        fids = sfids + dfids
        if fids:
            self.waicloader.set_fidlist(fids)
            self.waicloader.load(midlist, mid2info)
            self.waicloader.print_log()
            self.waicloader.reset()

        # 基础过滤
        basicfilter_config = self.config.get("Filter", "BasicFilterList")
        basic_pipeline = Pipeline()
        basic_pipeline.init_from_config(basicfilter_config)
        midlist = basic_pipeline.check(midlist, mid2info)
        basic_pipeline.print_log()
        basic_pipeline.reset()

        # 写入cache_file
        cfilename = self.config.get("Basic", "CacheFile")
        cMode = self.config.get("Basic", "CacheMode", fallback="w")
        cachef = CacheFile()
        cachef.write2file(cfilename, midlist, mid2info, mode=cMode)

        # assert len(midlist) == len(mid2info)
        return midlist, mid2info
