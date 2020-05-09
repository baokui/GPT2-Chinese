path_source=data/test_prosepoem.txt
path_target=rest/test_prosepoem_epoch70.json
nohup python -u gpt_gen_prosepoemp.py $path_source $path_target >> log/pp.log 2>&1 &