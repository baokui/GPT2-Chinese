mode=char
path_data=../data/userdata
path_target=../data/userdata_mergedmodel
path_vocab=../train/model/model_merged/vocab.txt
mkdir $path_target
padding=1
for((j=0;j<10;j++))
do
    for((i=0;i<9;i++))
    do
        idx=$j$i
        name=$idx.txt
        nohup python -u datapro_userdata_mergemodel.py $path_data $idx $name $path_target $path_vocab $padding >> log/datapro-userdata-$name.log 2>&1 &
    done
    i=9
    idx=$j$i
    name=$idx.txt
    nohup python -u datapro_userdata_mergemodel.py $path_data $idx $name $path_target $path_vocab $padding >> log/datapro-userdata-$name.log 2>&1
done