path_source=result/input3.txt
mode=0

path_config=demo_config/config_godText_large1.json
path_target=final
topk=10
temp=0.7
nohup python -u test_generator.py $mode $path_config $path_source result/$path_target-$topk-$temp.json $topk $temp >> log/test-gen-$path_target-$topk-$temp.log 2>&1 &

topk=8
temp=0.7
nohup python -u test_generator.py $mode $path_config $path_source result/$path_target-$topk-$temp.json $topk $temp >> log/test-gen-$path_target-$topk-$temp.log 2>&1 &


topk=6
temp=0.7
nohup python -u test_generator.py $mode $path_config $path_source result/$path_target-$topk-$temp-1.json $topk $temp >> log/test-gen-$path_target-$topk-$temp-1.log 2>&1 &

topk=4
temp=0.7
nohup python -u test_generator.py $mode $path_config $path_source result/$path_target-$topk-$temp.json $topk $temp >> log/test-gen-$path_target-$topk-$temp.log 2>&1 &


topk=10
temp=0.8
nohup python -u test_generator.py $mode $path_config $path_source result/$path_target-$topk-$temp.json $topk $temp >> log/test-gen-$path_target-$topk-$temp.log 2>&1 &
