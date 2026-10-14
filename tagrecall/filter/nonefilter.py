# _*_ coding: utf-8 _*_
# @Time    : 2019/10/16 4:18 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : nonefilter.py
# 不存在过滤器，特征不存在或者为空则过滤

import os
from .filter import Filter, del_count

class NoneFilter(Filter):

    def __init__(self, name, *args, **kwargs):
        super(NoneFilter, self).__init__(name, *args, **kwargs)
        # 特征名称
        self.fid = kwargs["fid"]
        # 可选：被过滤掉的 mid 导出的文件路径（用于排查物料问题）
        self.dump_file = kwargs.get("dump_file", "")
        self._dump_fh = None

    def _dump(self, mid, reason, midinfo):
        if not self.dump_file:
            return
        if self._dump_fh is None:
            parent = os.path.dirname(self.dump_file)
            if parent and not os.path.isdir(parent):
                os.makedirs(parent, exist_ok=True)
            self._dump_fh = open(self.dump_file, "w", encoding="utf-8")
        # 格式：mid \t fid \t 过滤原因 \t status \t created_at \t expired_at \t updated_at
        status = midinfo.get("status", "")
        created_at = midinfo.get("created_at", "")
        expired_at = midinfo.get("expired_at", "")
        updated_at = midinfo.get("updated_at", "")
        self._dump_fh.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            mid, self.fid, reason, status, created_at, expired_at, updated_at))

    def reset(self):
        super(NoneFilter, self).reset()
        if self._dump_fh is not None:
            self._dump_fh.flush()

    def __del__(self):
        if self._dump_fh is not None:
            try:
                self._dump_fh.close()
            except Exception:
                pass

    @del_count
    def check(self, mid, midinfo):
        # 依次区分三种过滤原因，便于排查物料问题
        if self.fid not in midinfo:
            # 特征不存在
            self._dump(mid, "fid_not_exist", midinfo)
            return False
        val = midinfo[self.fid]
        if not val:
            # 特征值为空（空字符串 / 0 / None）
            self._dump(mid, "value_empty", midinfo)
            return False
        if val == "NULL":
            # 特征值为字符串 "NULL"
            self._dump(mid, "value_NULL", midinfo)
            return False
        return True