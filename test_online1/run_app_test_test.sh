mode=$1
parallels=$2
time=$(date "+%Y-%m-%d--%H:%M:%S")
if [ $mode -eq 2 ]
then
    for((i=0;i<$parallels;i++))
    do
        path_data=data/test.txt
        path_target=result/tmp-$i.json
        path_log=log/apptest-post-$time-$parallels-$i.log
        nohup python -u app_test_post.py $path_data $path_target $path_log gou >> log/tmp.log 2>&1 &
    done
fi
#sh run_app_test_test.sh 2 20


#20 servers 20/30 parallels (有些无结果，空)
#16 servers 20 parrallels (有空结果）

#ps -ef|grep "app.py gou 20"|grep -v grep|awk  '{print "kill -9 " $2}' |sh
#sh run_app_batch.sh 12 gou 4
#sh run_app_test_start.sh 2 12
#sh run_app_test_test.sh 2 20