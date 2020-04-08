path_source=data/input.txt
'''
name=pretrained
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
#nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &
'''

name=dabaigou
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &
'''
name=dabaigou_pre
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=dabaigou_seg
path_config=config/config_$name.json
mode=seg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=godText
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=raw_godText
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=raw_godText_pad
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &

name=raw_godText_large
path_config=config/config_$name.json
mode=noseg
path_target=result/$name.json
nohup python -u testing.py $path_config $mode $path_source $path_target >> log/testing-$name.log 2>&1 &
'''