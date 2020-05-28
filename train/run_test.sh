path_config="config/config_comments2.json"
path_source="data/test_taobao.txt"
path_target="data/test.json"
nohup python -u test.py $path_config $path_source $path_target >> log/test.log 2>&1 &