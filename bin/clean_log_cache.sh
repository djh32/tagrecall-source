#!/bin/bash
# clean dir sh, per daily,不要使用系统默认字段 PATH、DIR
path=/data1/lijiang/tagrecall2

# clean log
find $path/logs/* -mtime +14 -delete

# clean cache
find $path/cache/* -mtime +7 -delete