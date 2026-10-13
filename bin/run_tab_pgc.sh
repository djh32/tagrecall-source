#!/bin/bash
PY='/data1/anaconda3/bin/python3.7'
DIR='/data1/lijiang/tagrecall2'

# shellcheck disable=SC2006
dt=`date -d "0 days ago" +%Y%m%d`

nohup $PY -u $DIR/tagrecall/scripts/run_redis_byKey_worker.py tab.rec.redis_byKey.ini >> $DIR/logs/tab.pgc.log_${dt} 2>&1 &

## clean log
#find $DIR/logs/* -mtime +28 -delete