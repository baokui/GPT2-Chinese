mode=char
path_data=../data/userdata
path_target=../data/userdata_tokenized_padding
mkdir $path_target
padding=1
for((j=0;j<10;j++))
do
    for((i=0;i<9;i++))
    do
        idx=$j$i
        name=$idx.txt
        nohup python -u datapro_userdata.py $mode $path_data $idx $name $path_target $padding >> log/datapro-userdata-$name.log 2>&1 &
    done
    i=9
    idx=$j$i
    name=$idx.txt
    nohup python -u datapro_userdata.py $mode $path_data $idx $name $path_target $padding >> log/datapro-userdata-$name.log 2>&1
done