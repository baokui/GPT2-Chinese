path_config="config/config_comments.json"
path_source="data/test.txt"
path_target="data/test.json"
nohup python -u test.py $path_config $path_source $path_target >> log/test.log 2>&1 &