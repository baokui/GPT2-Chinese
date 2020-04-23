path_data=data/test.txt
parallels=2
time=$(date "+%Y-%m-%d--%H:%M:%S")

sym=0
path_target=result/tmp-$sym.json
path_log=log/apptest-post-$time-$parallels-$sym.log
nohup python -u test_app_gevent.py $path_data $path_target $path_log $sym >> log/tmp-gen-$sym.log 2>&1 &

sym=index
path_target=result/tmp-$sym.json
path_log=log/apptest-post-$time-$parallels-$sym.log
nohup python -u app_test_post.py $path_data $path_target $path_log $sym >> log/tmp-gen-$sym.log 2>&1 &