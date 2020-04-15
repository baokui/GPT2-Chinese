path_source=../data/GodText/merge/godText_noXinNian.json
path_target=../data/GodText_tokenized_padding
mkdir $path_target
padding=1
path_vocab=../model/model_godText_pretrain/vocab.txt
nb_piece=20
n_ctx=64
nohup python -u datapro_godText.py $path_source $path_target $padding $path_vocab $nb_piece $n_ctx >> log/godText-padding.log 2>&1 &

path_source=../data/GodText/merge/godText_noXinNian.json
path_target=../data/GodText/Tokenized_data/
mkdir $path_target
padding=0
path_vocab=../model/model_godText_finetune/vocab.txt
nb_piece=10
n_ctx=64
nohup python -u datapro_godText.py $path_source $path_target $padding $path_vocab $nb_piece $n_ctx >> log/godText-padding.log 2>&1 &
