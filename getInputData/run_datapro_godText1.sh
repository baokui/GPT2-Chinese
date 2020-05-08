path_source=/search/odin/user/guobk/vpa-godText/Spyder/data_all/data_merged.json
path_target=/search/odin/user/guobk/vpa-godText/Spyder/data_tokenized_padding
mkdir $path_target
padding=1
path_vocab=../bin/model/model_godText_pretrain3_finetune_mergedata/vocab.txt
nb_piece=20
n_ctx=64
nohup python -u datapro_godText.py $path_source $path_target $padding $path_vocab $nb_piece $n_ctx >> log/godText-padding.log 2>&1 &
