nb_models=2
path_source=data/test_text.txt
path_target=result/test_text.json
nohup python -u test_compare.py $nb_models $path_source $path_target >> log/compare.log 2>&1 &