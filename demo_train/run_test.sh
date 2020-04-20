path_source=data/test_cut.txt
path_target=result/test_text-godTextPretrain.json
path_config=demo_config/config_dabaigou_new.json,demo_config/config_dabaigou.json,demo_config/config_godText_pretrain.json
doPredict=1,1,0,0
gpus=0,1
nohup python -u test.py $path_source $path_target $path_config $doPredict $gpus >> log/test_text-test.log 2>&1 &
