# _*_ coding: utf-8 _*_
# @Time    : 2019/10/8 5:20 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : waicreader.py

import traceback
from multiprocessing import Pool
from vcore.python.utils.waicapis import WAICApis

def read_mid_feas(midlist, fidstr, api = None, name = "aliyun", timeout = 3):
    if not api:
        api = WAICApis(name)

    # 节约链接数量
    session = api.get_session()
    tmp_mids = []
    result = {}
    for mid in midlist:
        tmp_mids.append(mid)
        if len(tmp_mids) >= 40:
            midstr = ",".join(tmp_mids)
            try:
                ret = api.get_mid_features(midstr, fidstr, timeout, session)
            except Exception as e:
                traceback.print_exc()
                ret = {}
            result.update(ret)
            tmp_mids.clear()

    if tmp_mids:
        midstr = ",".join(tmp_mids)
        try:
            ret = api.get_mid_features(midstr, fidstr, timeout, session)
        except Exception as e:
            traceback.print_exc()
            ret = {}
        result.update(ret)
        tmp_mids.clear()

    return result

def read_uid_feas(uidlist, fidstr, api = None, name = "aliyun", timeout = 3):
    if not api:
        api = WAICApis(name)

    # 节约链接数量
    session = api.get_session()
    tmp_uids = []
    result = {}
    for uid in uidlist:
        tmp_uids.append(uid)
        if len(tmp_uids) >= 40:
            uidstr = ",".join(tmp_uids)
            try:
                ret = api.get_user_features(uidstr, fidstr, timeout, session)
            except Exception as e:
                traceback.print_exc()
                ret = {}
            result.update(ret)
            tmp_uids.clear()

    if tmp_uids:
        uidstr = ",".join(tmp_uids)
        try:
            ret = api.get_user_features(uidstr, fidstr, timeout, session)
        except Exception as e:
            traceback.print_exc()
            ret = {}
        result.update(ret)
        tmp_uids.clear()

    return result



class WAICReader(object):

    def __init__(self, name="aliyun"):
        self.name = name
        self.apis = WAICApis(name)

    def read_obj_feas(self, objlist, fidlist, timeout = 3):
        idstr = ",".join(objlist)
        fidstr = ",".join(fidlist)
        try:
            ret = self.apis.get_object_features(idstr, fidstr, timeout)
        except Exception as e:
            traceback.print_exc()
            ret = {}
        return ret

    def read_uid_feas(self, uidlist, fidlist, timeout = 3):
        fidstr = ",".join(fidlist)
        result = read_uid_feas(uidlist, fidstr, api=self.apis, timeout=timeout)
        return result

    def read_mid_feas(self, midlist, fidlist, timeout = 3):
        fidstr = ",".join(fidlist)
        result = read_mid_feas(midlist, fidstr, api=self.apis, timeout=timeout)
        return result

    def mt_read_mid_feas(self, midlist, fidlist, process_num = 10, timeout = 3):
        '''
        多线程读取midlist的特征
        :param midlist:
        :param fidlist:
        :param process_num: 进程数量
        :return: [{'4421599799800146': {'10482': '...', '10484': '', ...}, {....}, ]
        '''
        if len(midlist) > 50000:
            midchunks = WAICReader.chunks(midlist, process_num * 10)
        else:
            midchunks = WAICReader.chunks(midlist, process_num)
        fidstr = ",".join(fidlist)
        params = [(chunk, fidstr, None, self.name, timeout) for chunk in midchunks]

        print("multi-process number: ", process_num)
        print("multi-process job number: ", len(params))

        with Pool(processes=process_num) as pool:
            result = pool.starmap(read_mid_feas, params)
        return result

    @staticmethod
    def chunks(l, n):
        n = max(1, n)
        batchn = int(len(l) / (n + 1) + 1)
        return (l[i:i+batchn] for i in range(0, len(l), batchn))

