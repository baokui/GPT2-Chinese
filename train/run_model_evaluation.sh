path_config=config/config_comments3.json
path_data=data/test_taobao.txt
nohup python -u model_evalution.py $path_config $path_data >> log/eval.log 2>&1 &

path_config=config/config_mergemodel.json
path_data=data/replace_gt_10.txt
nohup python -u model_evalution.py $path_config $path_data >> log/eval.log 2>&1 &