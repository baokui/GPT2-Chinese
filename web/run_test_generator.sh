path_source=../cgi-bin/data/input3.txt
mode=0

path_config=config/config_godText_large1.json
path_target=final
nohup python test_generator.py $mode $path_config $path_source result/$path_target.json >> log/test-gen-$path_target.log 2>&1 &

path_config=config/config_godText_large1_17.json
path_target=model_epoch17
nohup python test_generator.py $mode $path_config $path_source result/$path_target.json >> log/test-gen-$path_target.log 2>&1 &
