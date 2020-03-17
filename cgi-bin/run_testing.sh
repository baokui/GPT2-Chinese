path_configs = ['config_pretrained.json','config_raw_multiReplace.json','config_dabaigou.json','config_dabaigou_seg.json']

mkdir result

path_source=input.txt
name=pretrained
path_config=config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=dabaigou
path_config=config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=dabaigou_seg
path_config=config_$name.json
mode=seg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=raw_multiReplace
path_config=config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=raw_multiReplace_150w
path_config=config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &
