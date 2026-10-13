#!/bin/bash
PY='/data1/anaconda3/bin/python3.7'
DIR='/data1/lijiang/tagrecall2'

# shellcheck disable=SC2006
dt=`date -d "0 days ago" +%Y%m%d`

nohup $PY -u $DIR/tagrecall/scripts/run_default_worker.py tab.rec.ini >> $DIR/logs/tab.rec.log_${dt} 2>&1 &

## clean log
#find $DIR/logs/* -mtime +28 -delete