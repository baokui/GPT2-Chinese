path_gou=../data/GodText_tokenized_padding_finetune2
path_godText=../data/GodText_tokenized_padding
path_target=../data/GodText_tokenized_padding_finetune2_merged
mkdir $path_target
nohup python -u dataMergeGouGodText.py $path_gou $path_godText $path_target >> log/merge.log 2>&1 &