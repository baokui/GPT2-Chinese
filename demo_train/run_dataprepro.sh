path_source=data/
path_target=data_tokenized
mkdir $path_target
mkdir log
padding=1
path_vocab=model/modelexample/vocab.txt
n_ctx=64
nohup python -u dataprepro.py $path_source $path_target $padding $path_vocab $n_ctx >> log/godText-padding.log 2>&1 &
