mode=char
path_data=../data/userdata

for((j=0;j<10;j++))
do
    for((i=0;i<9;i++))
    do
        idx=$j$i
        name=$idx.txt
        nohup python -u datapro_userdata.py $mode $path_data $idx $name >> log/datapro-userdata-$name.log 2>&1 &
    done
    i=9
    idx=$j$i
    name=$idx.txt
    nohup python -u datapro_userdata.py $mode $path_data $idx $name >> log/datapro-userdata-$name.log 2>&1
done
