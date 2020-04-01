path_source=result/input4.txt
mode=2

path_config=demo_config/config_godText_large1.json
path_target=final
topk=5
temp=0.5
nohup python -u test_generator.py $mode $path_config $path_source result/$path_target-$topk-$temp-$mode.json $topk $temp >> log/test-gen-$path_target-$topk-$temp-$mode.log 2>&1 &
