# _*_ coding: utf-8 _*_
# @Time    : 2021/1/29 11:19 AM
# @Author  : lijiang3@staff.weibo.com
# @File    : test_mysql_scanner.py

from tagrecall.scan.scanner_mysql import MysqlScanner

if __name__ == "__main__":

    scanner = MysqlScanner("m9747i.eos.grid.sina.com.cn", 9747, "db_video", "video_material_recom_online")
    scanner.get_mids_test()