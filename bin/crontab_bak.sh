ip=$1
user=$USER
rd=`date +%Y%m%d%H`
bakname=data/crontab.$ip.$user.$rd.txt

echo $rd $user
crontab -l > ${bakname}

find data/* -mtime +14 -delete