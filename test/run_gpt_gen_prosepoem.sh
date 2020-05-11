path_source=data/test_prosepoem.txt
path_target=result/test_prosepoem_final.json
nohup python -u gpt_gen_prosepoemp.py $path_source $path_target >> log/pp.log 2>&1 &