path_source=data/input3.txt
name=dabaigou
path_config=../web/demo_config/config_$name.json
mode=noseg
fp16=1
modeType=dabaigou
path_target=result/$name-$fp16.json
nohup python -u testing.py $path_config $mode $path_source $path_target $fp16 $modeType >> log/testing-$name-$fp16.log 2>&1 &

fp16=0
modeType=dabaigou
path_target=result/$name-$fp16.json
nohup python -u testing.py $path_config $mode $path_source $path_target $fp16 $modeType >> log/testing-$name-$fp16.log 2>&1 &
