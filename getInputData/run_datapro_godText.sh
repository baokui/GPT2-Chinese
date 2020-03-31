path_source=../data/godText_all1.json
path_target=../data/godText_tokenized_padding
mkdir $path_target
padding=1
nohup python -u datapro_godText.py $path_source $path_target $padding >> log/godText-padding.log 2>&1 &