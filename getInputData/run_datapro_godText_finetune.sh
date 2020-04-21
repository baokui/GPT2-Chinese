path_target=../data/GodText_tokenized_padding_finetune
mkdir $path_target
padding=1
path_vocab=../model/model_godText_pretrain/vocab.txt
nb_piece=50
n_ctx=64
for((i=0;i<10;i++))
do
path_source=../data/dabaigou/000$i
sym=sym$i-
nohup python -u datapro_godText_finetune.py $path_source $path_target $padding $path_vocab $nb_piece $n_ctx $sym >> log/godText-padding-finetune-$i.log 2>&1 &
done
