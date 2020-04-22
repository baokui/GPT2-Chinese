mode=$1
gpus=$2
N=$3
time=$(date "+%Y-%m-%d--%H:%M:%S")
if [ $mode -eq 1 ]
then
    #ps -ef|grep app_test|grep -v grep|awk  '{print "kill -9 " $2}' |sh
    nohup python -u app_test.py 7000 $gpus >> log/apptest-7000.log 2>&1 &
else
    for((i=0;i<$N;i++))
    do
        s="'"
        t="\""
        #inputStr=input
        #param=$s{$t$inputStr$t:$i}$s
        #nohup curl http://127.0.0.1:7000/api/gen_test -d $param -X POST >> log/apptest-post-$N-$i.log 2>&1 &
        #echo http://127.0.0.1:7000/api/gen_test -d $param -X POST

        path_data=data/test.txt
        path_target=result/tmp-$i.json
        path_log=log/apptest-post-$time.log
        mode=gen
        #nohup python -u app_test_post.py $path_data $path_target $path_log $mode >> log/tmp.log 2>&1 &

        path_data=aaa
        path_target=bbb
        path_log=log/app_testmode-$i.log
        mode=test
        rm -rf log/app_testmode-$i.log
        nohup python -u app_test_post.py $path_data $path_target $path_log $mode >> $path_log 2>&1 &

    done
fi