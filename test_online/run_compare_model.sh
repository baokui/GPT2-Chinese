path_configs=demo_config/config_godText_large1.json,demo_config/config_godText_small.json
path_source=data/test_cut.txt
path_target=result/test_cutjson
nohup python -u test_compare_model.py $path_configs $path_source $path_target >> ./log/compare_model.log 2>&1 &
