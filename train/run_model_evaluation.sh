path_config=config/config_comments3.json
path_data=data/test_taobao.txt
nohup python -u model_evaluation.py $path_config $path_data >> log/eval.log 2>&1 &