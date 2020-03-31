mode=char
path_data=../data/userdata
path_target=../data/userdata_vocab
mkdir $path_target
for((j=0;j<10;j++))
do
    for((i=0;i<9;i++))
    do
        idx=$j$i
        name=$idx.txt
        nohup python -u getVocab.py $path_data $path_target/vocab-$name $idx >> log/vocab-$idx.log 2>&1 &
    done
    i=9
    idx=$j$i
    name=$idx.txt
    nohup python -u getVocab.py $path_data $path_target/vocab-$name $idx >> log/vocab-$idx.log 2>&1
done
