path_config=config/config_comments3.json
path_data=data/test_taobao.txt
nohup python -u model_evalution.py $path_config $path_data >> log/eval.log 2>&1 &

path_config=config/config_mergemodel.json
path_data=data/replace_gt_10_small.txt
gpu=3
mask=MASK_gou,MASK_prose
nohup python -u model_evalution.py $path_config $path_data $gpu $mask >> log/eval.log 2>&1 &

path_config=/search/odin/vpaTextGenerating/bin/config/config_godText_large1_compressed.json
path_data=data/replace_gt_10_small.txt
gpu=2
mask=MASK
nohup python -u model_evalution.py $path_config $path_data $gpu $mask >> log/eval-large.log 2>&1 &

path_config=/search/odin/vpaTextGenerating/bin/config/config_godText_small_finetune_merged.json
path_data=data/replace_gt_10_small.txt
gpu=1
mask=MASK
nohup python -u model_evalution.py $path_config $path_data $gpu $mask >> log/eval-small.log 2>&1 &
