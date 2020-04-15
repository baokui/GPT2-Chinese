path_source=data/test_text.txt
path_target=result/test_text-godTextPretrain.json
path_config=demo_config/config_godText_pretrain.json,demo_config/config_godText_pretrain.json,demo_config/config_godText_pretrain.json
doPredict=1,0,0,0
nohup python -u test.py $path_source $path_target $path_config $doPredict >> log/test_text-test.log 2>&1 &
