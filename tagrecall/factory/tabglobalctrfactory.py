# _*_ coding: utf-8 _*_
# @Time    : 2019/12/3 5:28 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : tabglobalctrfactory.py

import zlib
import json
import time
from .recallfactory import RecallFactory


def _get_stream_names(ret, impn, ts, threshold = 300, mode=""):
    """
    获取 top曝光量，观察推荐状态
    获取 曝光>=threshold, top ctr 和 tail ctr
    :param ret:
    :param impn:
    :param ts:
    :param threshold:
    :param mode:
    :return:
    """
    if mode in ("male", "female"):
        mode = "_%s" % mode

    if impn >= threshold:
        # Top点击率(7天真曝)
        ret.append(("top_ctr" + mode, {}))
        # Tail最差点击率(7天真曝)
        ret.append(("tail_ctr" + mode, {}))
        # Top 曝光(7天真曝)
        ret.append(("top_vv" + mode, {}))

        current = int(time.time())
        if (current - ts <= 24 * 3600):
            # 1天内发布物料，Top点击率(7天真曝)
            ret.append(("top_ctr_1day" + mode, {}))
            # 1天内发布物料，Top最差点击率(1天真曝)
            ret.append(("tail_ctr_1day" + mode, {}))
            # 1天内发布物料，Top 曝光
            ret.append(("top_vv_1day" + mode, {}))

        if (current - ts <= 7 * 24 * 3600):
            # 1~7天发布物料里，Top点击率(7天真曝)
            ret.append(("top_ctr_7day" + mode, {}))
            # 1~7天发布物料里，Top最差点击率(7天真曝)
            ret.append(("top_ctr_7day" + mode, {}))
            # 1天内发布物料，Top 曝光
            ret.append(("top_vv_7day" + mode, {}))


def _fill_stream_score(stream_name, stream, mid2info, pub_dt="", mode=""):
    """
    10776(7天曝光) 10777(7天点击) 10698(24h曝光) 10700(24h点击)
    "10824",  //Tab男性的真实点击数_离线更新7天内数据
    "10825",  //Tab男性的真实曝光数_离线更新7天内数据
    "10831",  //Tab女性的真实点击数_离线更新7天内数据
    "10832",  //Tab女性的真实曝光数_离线更新7天内数据
    "100034",	//推荐流的总曝光数、播放时长、播放数(0～3s)、播放数(>=20s）、播放数(>=50%)、播放数(>=90%)
    "100035",	//推荐流的粉丝的总曝光数、播放时长、播放数(0～3s)、播放数(>=20s）、播放数(>=50%)、播放数(>=90%)
    发布时间满足pub_dt 需求的 7天ctr和曝光数据
    :param pub_dt: ""-整体发布物料，"1d" 1天内发布物料，"7d"7天内发布物料
    :param mode: "" All user, "male" male user, "female" female user
    :return:
    """
    fill_stream_name = {}

    if mode == "male":
        imp_fid = "10825"
        clk_fid = "10824"
        mode = "_male"
    elif mode == "female":
        imp_fid = "10832"
        clk_fid = "10831"
        mode = "_female"
    else:
        imp_fid = "10776"
        clk_fid = "10777"
        mode = ""

    if pub_dt == "1d":
        fill_stream_name = {
            "top_ctr": "top_ctr_1day" + mode,
            "tail_ctr": "tail_ctr_1day" + mode,
            "top_vv": "top_vv_1day" + mode
        }
    elif pub_dt == "7d":
        fill_stream_name = {
            "top_ctr": "top_ctr_7day" + mode,
            "tail_ctr": "tail_ctr_7day" + mode,
            "top_vv": "top_vv_7day" + mode
        }
    else:
        fill_stream_name = {
            "top_ctr": "top_ctr" + mode,
            "tail_ctr": "tail_ctr" + mode,
            "top_vv": "top_vv" + mode
        }

    if fill_stream_name["top_ctr"] == stream_name:
        for mid, detail in stream.midlist:
            imp = int(mid2info[mid].get(imp_fid, 0))
            clk = int(mid2info[mid].get(clk_fid, 0))
            score = clk / imp
            stream.midwithscore.append((mid, score))
        stream.midwithscore = sorted(stream.midwithscore, reverse=True, key=lambda x: x[1])

    elif fill_stream_name["tail_ctr"] == stream_name:
        for mid, detail in stream.midlist:
            imp = int(mid2info[mid].get(imp_fid, 0))
            clk = int(mid2info[mid].get(clk_fid, 0))
            score = clk / imp
            stream.midwithscore.append((mid, score))
        stream.midwithscore = sorted(stream.midwithscore, reverse=False, key=lambda x: x[1])

    elif fill_stream_name["top_vv"] == stream_name:
        for mid, detail in stream.midlist:
            imp = int(mid2info[mid].get(imp_fid, 0))
            score = imp
            stream.midwithscore.append((mid, score))
        stream.midwithscore = sorted(stream.midwithscore, reverse=True, key=lambda x: x[1])
    else:
        pass


class TabGlobalCtrFactory(RecallFactory):
    """
     10776(7天曝光) 10777(7天点击) 10698(24h曝光) 10700(24h点击)
    "10824",  //Tab男性的真实点击数_离线更新7天内数据
    "10825",  //Tab男性的真实曝光数_离线更新7天内数据
    "10831",  //Tab女性的真实点击数_离线更新7天内数据
    "10832",  //Tab女性的真实曝光数_离线更新7天内数据
    "100034",	//推荐流的总曝光数、播放时长、播放数(0～3s)、播放数(>=20s）、播放数(>=50%)、播放数(>=90%)
    "100035",	//推荐流的粉丝的总曝光数、播放时长、播放数(0～3s)、播放数(>=20s）、播放数(>=50%)、播放数(>=90%)
    """

    def __init__(self, **kwargs):
        super(TabGlobalCtrFactory, self).__init__(**kwargs)

    def get_streaminfo_list(self, mid, minfo):
        impn = minfo.get("10776", 0)
        impn_male = minfo.get("10825", 0)
        impn_female = minfo.get("10832", 0)
        ts = minfo["ts"]
        ret = []

        # 整体top tail ctr, top vv, 曝光量>500
        _get_stream_names(ret, impn, ts, mode="")
        _get_stream_names(ret, impn_male, ts, mode="male")
        _get_stream_names(ret, impn_female, ts, mode="female")

        return ret

    def rank(self, stream_name, stream, mid2info):
        # 全部发布物料
        _fill_stream_score(stream_name, stream, mid2info)
        _fill_stream_score(stream_name, stream, mid2info, mode="male")
        _fill_stream_score(stream_name, stream, mid2info, mode="female")
        # 1天内发布物料
        _fill_stream_score(stream_name, stream, mid2info, pub_dt="1d")
        _fill_stream_score(stream_name, stream, mid2info, pub_dt="1d", mode="male")
        _fill_stream_score(stream_name, stream, mid2info, pub_dt="1d", mode="female")
        # 7天内发布物料
        _fill_stream_score(stream_name, stream, mid2info, pub_dt="7d")
        _fill_stream_score(stream_name, stream, mid2info, pub_dt="7d", mode="male")
        _fill_stream_score(stream_name, stream, mid2info, pub_dt="7d", mode="female")

    def after_rank(self, stream_name, stream, mid2info):
        '''
        排序后的处理。
        '''
        stream.midwithscore = stream.midwithscore[0:self.num]
        return

    def format(self, stream_name, stream, mid2info):
        '''
        格式化要写入redis的数据
        :param stream_name:
        :param stream:
        :param mid2info:
        :return:
        '''
        content = []

        for mid, score in stream.midwithscore:
            content.append({"mid":mid, "tab_score":str(round(score, 4))})
        if not content:
            return ""
        content = zlib.compress(json.dumps(content).encode("ascii"))
        return content
