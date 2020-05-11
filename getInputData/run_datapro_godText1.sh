path_source=/search/odin/user/guobk/vpa-godText/Spyder/data_merged/data_all_n_filter.json
path_target=/search/odin/user/guobk/vpa-godText/Spyder/data_tokenized_padding_n_proseModel
mkdir $path_target
padding=0
path_vocab=../bin/model/model_godText_large1/vocab.txt
nb_piece=20
n_ctx=1024
nohup python -u datapro_godText.py $path_source $path_target $padding $path_vocab $nb_piece $n_ctx >> log/godText-padding.log 2>&1 &
