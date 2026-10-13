# _*_ coding: utf-8 _*_
# @Time    : 2019/7/19 7:24 PM
# @Author  : lijiang3@staff.weibo.com
# @File    : midtool.py
#
# 处理mid的工具类


class MidTool(object):

    @staticmethod
    def get_ts(mid):
        '''
        从mid中拆解出发布时间
        :param mid:
        :return:
        '''
        return (int(mid) >> 22) + 515483463

if __name__ == "__main__":

    print(MidTool.get_ts("4395817198469207"))