# _*_ coding: utf-8 _*_
# @Time    : 2019/10/21 10:26 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : openapimidreader.py
# 调用OpenApis的show-batch接口

from datetime import datetime
from vcore.python.utils.openapis import OpenApis
from vcore.python.utils.midtool import MidTool
from multiprocessing import Pool

def get_videos_info(midlist, timeout):
    reader = MidReader()
    (ret, rawlist) = reader.get_videos(midlist, timeout)
    return ret

class MidReader(object):

    def __init__(self, name = "aliyun"):
        self.apis = OpenApis(name)

    @staticmethod
    def mt_get_videos(midlist, process_num = 10, timeout = 3):
        if len(midlist) > 50000:
            midchunks = MidReader.chunks(midlist, process_num * 10)
        else:
            midchunks = MidReader.chunks(midlist, process_num)
        params = [(chunk, timeout) for chunk in midchunks]

        print("multi-process number: ", process_num)
        print("multi-process job number: ", len(params))

        with Pool(processes=process_num) as pool:
            result = pool.starmap(get_videos_info, params)
        return result

    def get_videos(self, midlist, timeout=3, rawdata=False):
        '''
        调用show-batch接口，再解析出视频需要的字段
        :param midlist:
        :param timeout:
        :param rawdata: 是否返回原始数据
        :return:
        '''
        batch = []
        content = {}
        for mid in midlist:
            batch.append(mid)
            if len(batch) >= 45:
                midstr = ",".join(batch)
                batch_ret = self.apis.statuses_showbatch(midstr, timeout=timeout)
                content.update(batch_ret)
                batch = []

        if batch:
            midstr = ",".join(batch)
            batch_ret = self.apis.statuses_showbatch(midstr, timeout=timeout)
            content.update(batch_ret)

        ret = []
        rawlist = []
        for mid in midlist:
            midinfo = content.get(mid, {})
            vinfo = {"mid":mid}
            self._parse_basic(midinfo, vinfo)
            self._parse_video(midinfo, vinfo)
            ret.append(vinfo)
            if rawdata:
                rawlist.append(midinfo)
        return (ret, rawlist)

    def _parse_basic(self, midinfo, ret):
        '''
        抽取的特征都放到ret中
        :param midinfo:
        :param ret:
        :return:
        '''
        assert isinstance(ret, dict)
        if not midinfo or "mid" not in midinfo:
            return
        ret["mid"] = midinfo["mid"]
        ts = MidTool.get_ts(ret["mid"])
        ret["ts"] = ts
        ret["create"] = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        ret["text"] = midinfo["text"]
        if "user" in midinfo:
            ret["uid"] = midinfo["user"]["id"]
            ret["name"] = midinfo["user"]["name"]
        if "deleted" in midinfo:
            ret["deleted"] = 1
            return
        ret["reposts"] = int(midinfo.get("reposts_count", 0))
        ret["comments"] = int(midinfo.get("comments_count", 0))
        ret["attitudes"] = int(midinfo.get("attitudes_count", 0))

    def _parse_video(self, midinfo, ret):
        '''
        提取视频有关的属性
        :param midinfo:
        :param ret:
        :return:
        '''
        assert isinstance(ret, dict)
        if not midinfo or "mid" not in midinfo:
            return
        url_objects = midinfo.get("url_objects", [])
        if not url_objects:
            return
        video_obj = None
        for obj in url_objects:
            if "object" in obj and obj["object"].get("object_type", "") == "video":
                video_obj = obj
                break
        if not video_obj:
            return

        outer_obj = video_obj["object"]
        ret["oid"] = outer_obj["object_id"]
        inner_obj = outer_obj.get("object", {})

        if inner_obj.get("titles", []):
            ret["title"] = inner_obj["titles"][0].get("title", "")

        if "duration" in inner_obj:
            ret["dura"] = int(inner_obj["duration"])

        cover = inner_obj.get("image", {}).get("url", "")
        if not cover:
            cover = inner_obj.get("screenshots", {}).get("1", "")
        ret["cover"] = cover

    @staticmethod
    def chunks(l, n):
        n = max(1, n)
        batchn = int(len(l) / (n + 1) + 1)
        return (l[i:i+batchn] for i in range(0, len(l), batchn))
