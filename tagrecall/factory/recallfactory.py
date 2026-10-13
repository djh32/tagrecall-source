# _*_ coding: utf-8 _*_
# @Time    : 2019/10/17 2:58 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : recallfactory.py
# 生成召回流的工厂

import logging
import time
from datetime import datetime
import json
import zlib
from collections import defaultdict
from vcore.python.utils.redisproxy import RedisProxy

class RecallStream(object):

    def __init__(self, name):
        self.name = name
        # 格式：[(mid, detail), ...]
        self.midlist = []
        self.midwithscore = []

class RecallFactory(object):

    def __init__(self, **kwargs):
        '''
        参数： prefix = "", version = "", num = 300, redis_addr = ["rm51826.eos.grid.sina.com.cn", 51826, 9, False], expire_time = 30 * 24 * 3600
        :param kwargs:
        '''
        self.flag = kwargs.get("flag", "")
        self.dry_run = self._str2bool(kwargs.get("dry_run", False))
        self.prefix = kwargs.get("prefix", "")
        self.version = kwargs.get("version", "")
        # 每个召回流里面的物料数量
        self.num = int(kwargs["num"])
        self.rproxy = RedisProxy()
        redis_addr = kwargs["redis_addr"]
        if isinstance(redis_addr, str):
            redis_addr = json.loads(redis_addr)
        self.rproxy.new_pool_list("writer", [redis_addr])
        # 召回流过期时间
        self.expire_time = kwargs.get("expire_time", 7 * 24 * 3600)
        self.streams = {}

        self.counter = defaultdict(int)

    @staticmethod
    def _str2bool(val):
        if isinstance(val, bool):
            return val
        return str(val).strip().lower() in ("1", "true", "yes", "on")

    def get_streaminfo_list(self, mid, minfo):
        '''
            判断一个mid应该放到哪些流里面
            一个mid可以放到多个recall-stream里面
            返回的streaminfo: (name, detail)
        '''
        return []

    def before_rank(self, mid2info):
        '''
        开始排序之前做一些准备工作
        例如读取一些redis资源
        :param mid2info:
        :return:
        '''
        pass

    def pre_rank(self, stream_name, stream, mid2info):
        '''
        排序前的处理
        可以再通过规则过滤掉一些mid
        或者为后续的排序做准备工作
        :param stream:
        :param mid2info:
        :return:
        '''
        pass

    def rank(self, stream_name, stream, mid2info):
        '''
        排序函数: 默认取全局排序的score
        :param stream:
        :param mid2info:
        :return:
        '''
        for mid, detail in stream.midlist:
            score = mid2info[mid].get("default_score", 0)
            stream.midwithscore.append((mid, score))

        stream.midwithscore = sorted(stream.midwithscore, reverse=True, key=lambda x:x[1])

    def after_rank(self, stream_name, stream, mid2info):
        '''
        排序后的处理。
        默认需要过滤相同的gid，需要截断操作。
        默认要过滤掉 gid=""(取不到的情况)
        10988: 是最新的gid
        :param stream:
        :param mid2info:
        :return:
        '''
        tmp = []
        gidset = set()
        for mid, score in stream.midwithscore:
            # 没有gid或者gid已出现
            gid = mid2info[mid].get("10988", "")
            if not gid or gid in gidset:
                continue
            # 没有被过滤掉
            tmp.append((mid, score))
            if len(tmp) >= self.num:
                break
            gidset.add(gid)

        stream.midwithscore = tmp
        return

    def format(self, stream_name, stream, mid2info):
        '''
        格式化要写入redis的数据
        :param stream_name:
        :param stream:
        :param mid2info:
        :return:
        '''
        return ""

    def handle(self, midlist, mid2info):
        '''
        生成各式各样的召回候选流
        然后写入到redis
        :param midlist:
        :param mid2info:
        :return:
        '''

        # 分配mid到各个stream中
        for mid in midlist:
            minfo = mid2info.get(mid, {})
            streaminfo_list = self.get_streaminfo_list(mid, minfo)
            for stream_name, detail in streaminfo_list:
                if stream_name not in self.streams:
                    self.streams[stream_name] = RecallStream(stream_name)

                stream = self.streams[stream_name]
                stream.midlist.append((mid, detail))

        self.before_rank(mid2info)

        # 每个stream做排序
        for stream_name, stream in self.streams.items():
            self.pre_rank(stream_name, stream, mid2info)
            self.rank(stream_name, stream, mid2info)
            self.after_rank(stream_name, stream, mid2info)

        # 所有stream写redis
        self.write(mid2info)

    def redis_key(self, stream_name):
        return self.prefix + stream_name + "_" + self.version if self.version else self.prefix + stream_name

    def write(self, mid2info):
        if self.dry_run:
            self._dry_run_write(mid2info)
            return
        # 所有stream写redis
        conn = self.rproxy.get_rand_connection("writer")
        pipe = conn.pipeline(transaction=False)
        count = 0
        for stream_name, stream in self.streams.items():
            rkey = self.redis_key(stream_name)
            rdata = self.format(stream_name, stream, mid2info)
            if not rdata:
                continue
            pipe.set(rkey, rdata, ex=self.expire_time)
            count += 1
            self.counter["stream_num"] += 1
            if count >= 50:
                pipe.execute()
                count = 0
                pipe = conn.pipeline(transaction=False)

        if count:
            pipe.execute()

        # 增加监控 eg: newtab_uid_v1_update
        alert_key = self.prefix + self.version + "_update"
        alert_data = int(time.time())
        pipe.set(alert_key, alert_data, ex=self.expire_time)
        pipe.execute()

    def _dry_run_write(self, mid2info):
        '''
        dry-run 模式：只生成倒排内容并打印预览，不写 redis、不写监控。
        逐条 key 打印会刷屏（如 TabTagFactory 有 19 万个 stream），因此这里只做：
        1) 汇总统计（stream 数、总条数、空流数、每流条数 min/avg/max）
        2) 有限采样（前 SAMPLES 个非空 stream 的 key/num/sample）
        '''
        SAMPLES = 5
        nums = []
        empty = 0
        samples = []
        for stream_name, stream in self.streams.items():
            rkey = self.redis_key(stream_name)
            rdata = self.format(stream_name, stream, mid2info)
            if not rdata:
                empty += 1
                continue
            self.counter["stream_num"] += 1
            try:
                items = json.loads(zlib.decompress(rdata))
                num = len(items) if isinstance(items, list) else -1
            except Exception:
                items = None
                num = -1
            nums.append(num)
            if len(samples) < SAMPLES:
                samples.append((rkey, num, items[0] if items else None))
        self._print_dry_run_summary(self.counter.get("stream_num", 0), nums, empty, samples)

    def _dry_run_write_single(self, mid2info):
        '''
        dry-run 模式：single-key 工厂预览（format 返回 list，非压缩 bytes）。
        不写 redis、不写监控。
        '''
        SAMPLES = 5
        nums = []
        empty = 0
        samples = []
        rkey = self.prefix + self.version
        for stream_name, stream in self.streams.items():
            items = self.format(stream_name, stream, mid2info)
            if not items:
                empty += 1
                continue
            num = len(items)
            nums.append(num)
            self.counter["stream_num"] += 1
            if len(samples) < SAMPLES:
                samples.append((rkey + "#" + stream_name, num, items[0] if items else None))
        self._print_dry_run_summary(self.counter.get("stream_num", 0), nums, empty, samples)

    def _print_dry_run_summary(self, stream_num, nums, empty, samples):
        logging.info("[DRY-RUN] ========== {} ==========".format(type(self).__name__))
        logging.info("[DRY-RUN] stream_num={} empty_stream_num={}".format(stream_num, empty))
        if nums:
            logging.info("[DRY-RUN] items per stream -> min={} avg={:.1f} max={}".format(
                min(nums), sum(nums) / len(nums), max(nums)))
            logging.info("[DRY-RUN] total items = {}".format(sum(nums)))
        for rkey, num, item in samples:
            logging.info("[DRY-RUN] sample key={} num={}".format(rkey, num))
            if item is not None:
                logging.info("[DRY-RUN] sample item={}".format(json.dumps(item, ensure_ascii=False)))
        logging.info("[DRY-RUN] ========== {} END ==========".format(type(self).__name__))


    def print_log(self):
        logging.info("******* recall-factory {0} statistic info {1} *********".format(type(self).__name__, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        logging.info("write recall-stream number: {}".format(self.counter.get("stream_num", 0)))
        #total_mid_count = self._valid_mid_count()
        #logging.info("mid number in recall-streams: {}".format(total_mid_count))

    def _valid_mid_count(self):
        midset = set()
        for stream_name, stream in self.streams.items():
            for mid, score in stream.midwithscore:
                midset.add(mid)
        return len(midset)