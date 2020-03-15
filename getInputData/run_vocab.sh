mode=vocab
for((idx0=0;idx0<4;idx0++))
do
    for((idx1=0;idx1<8;idx1++))
    do
        file=00$idx0$idx1
        path_source=../data/202002_seg/$file.txt
        path_target=../data/202002_seg_vocab/$file
        filename=$file
        nohup python -u sentsement.py $mode $path_source $path_target $filename >> log/seg-$mode-$file.log 2>&1 &
    done
    idx1=8
    file=00$idx0$idx1
    path_source=../data/202002_seg/$file.txt
    path_target=../data/202002_seg_vocab/$file
    filename=$file
    nohup python -u sentsement.py $mode $path_source $path_target $filename >> log/seg-$mode-$file.log 2>&1
done