path_data=../data/GodText/merge/godText_noXinNian.json
path_target=../data/godText_mergedmodel
path_vocab=../train/model/model_merged/vocab.txt
mkdir $path_target
padding=1
nohup python -u datapro_godText_mergemodel.py $path_data $path_target $path_vocab $padding >> log/datapro-godText.log 2>&1 &
