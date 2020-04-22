mode=$1
gpus=$2
N=$3
if [ $mode -eq 1 ]
then
    #ps -ef|grep app_test|grep -v grep|awk  '{print "kill -9 " $2}' |sh
    nohup python -u app_test.py 7000 $gpus >> log/apptest-7000.log 2>&1 &
else
    for((i=0;i<$N;i++))
    do
        nohup curl http://127.0.0.1:7000/api/gen_test -d '{"input":$i}' -X POST >> log/apptest-post-$N-$i.log 2>&1 &
    done
fi