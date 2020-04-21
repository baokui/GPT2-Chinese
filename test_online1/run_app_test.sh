mode=$1
if [ $mode -eq 1 ]
then
    nohup python -u app_test.py 6000 >> log/apptest-6000.log 2>&1 &
else
    for((i=0;i<10;i++))
    do
        nohup curl http://127.0.0.1:6000/api/gen_test -X POST >> log/apptest-post-$i.log 2>&1 &
    done
fi