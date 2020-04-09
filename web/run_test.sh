path_source=data/test_text.txt

penalty=1.2
path_target=result/test_text.json
gpus=0,1,2
onlyMax=0
nohup python -u test.py $path_source $path_target $gpus $penalty $onlyMax >> log/test_text-penalty-$penalty.log 2>&1 &

penalty=1.5
path_target=result/test_text-penalty=$penalty.json
gpus=3,4,5
#nohup python -u test.py $path_source $path_target $gpus $penalty >> log/test_text-penalty-$penalty.log 2>&1 &

