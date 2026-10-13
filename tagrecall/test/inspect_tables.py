# _*_ coding: utf-8 _*_
# 查看两张物料库表的结构、dt 及部分数据
import pymysql

MYSQL_USER = "db_video_wbrec_r"
MYSQL_PWD = "4f7c415aeeb5a62"
HOST = "m9747i.eos.grid.sina.com.cn"
PORT = 9747

TARGETS = [
    ("db_video", "video_material_recom_online"),
    ("material_new_arch", "dot_material_online"),
]


def inspect(db_name, table):
    conn = pymysql.connect(host=HOST, port=PORT, user=MYSQL_USER,
                           password=MYSQL_PWD, database=db_name,
                           connect_timeout=10)
    cur = conn.cursor()
    print("=" * 80)
    print("DATABASE: {}  TABLE: {}".format(db_name, table))

    # 1. 表结构
    cur.execute("DESC {}".format(table))
    print("---- schema ----")
    for row in cur.fetchall():
        print(row)

    # 2. 数据行数
    cur.execute("SELECT COUNT(*) FROM {}".format(table))
    print("---- row count ----")
    print(cur.fetchone()[0])

    # 3. dt 字段的取值范围（若存在 dt 列）
    cur.execute("DESC {}".format(table))
    cols = [r[0] for r in cur.fetchall()]
    dt_col = None
    for c in cols:
        if c.lower() in ("dt", "stat_date", "date", "day"):
            dt_col = c
            break
    print("---- dt column candidate ----")
    print(dt_col)
    if dt_col:
        try:
            cur.execute("SELECT MIN({0}), MAX({0}), COUNT(DISTINCT {0}) FROM {1}".format(dt_col, table))
            print("min/max/distinct of {}:".format(dt_col), cur.fetchone())
        except Exception as e:
            print("dt query failed:", e)

    # 4. 部分数据
    cur.execute("SELECT * FROM {} LIMIT 3".format(table))
    print("---- sample rows (limit 3) ----")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    for db, table in TARGETS:
        try:
            inspect(db, table)
        except Exception as e:
            print("=" * 80)
            print("INSPECT FAILED for {}.{}".format(db, table))
            print(type(e).__name__, e)
