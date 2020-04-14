path_source=data/test_text.txt
path_target=result/test_text-resort-20-test.json
path_config=demo_config/config_godText_large1.json,demo_config/config_poem.json,demo_config/config_dabaigou_small.json
nohup python -u test.py $path_source $path_target >> log/test_text-test.log 2>&1 &
