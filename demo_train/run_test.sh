path_source=data/test_text.txt
path_target=result/test_text-godTextPretrain.json
path_config=demo_config/config_dabaigou_new.json,demo_config/config_dabaigou.json,demo_config/config_dabaigou_new.json
doPredict=0,1,1,0
gpus=0,1,2
nohup python -u test.py $path_source $path_target $path_config $doPredict $gpus >> log/test_text-test.log 2>&1 &
