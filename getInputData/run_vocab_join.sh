mode=vocab_join0
for((idx0=0;idx0<4;idx0++))
do
    for((idx1=0;idx1<8;idx1++))
    do
        file=00$idx0$idx1
        path_source=../data/202002_seg_vocab/$file
        path_target=../data/202002_seg_vocab/join-$file.txt
        filename=$file
        nohup python -u sentsement.py $mode $path_source $path_target $filename >> log/seg-$mode-$file.log 2>&1 &
    done
    idx1=8
    file=00$idx0$idx1
    path_source=../data/202002_seg_vocab/$file
    path_target=../data/202002_seg_vocab/join-$file.txt
    filename=$file
    nohup python -u sentsement.py $mode $path_source $path_target $filename >> log/seg-$mode-$file.log 2>&1
done

mode=vocab_join_all
path_source=../data/202002_seg_vocab
path_target=../data/202002_seg_vocab/join-all.txt
nohup python -u sentsement.py $mode $path_source $path_target $filename >> log/seg-$mode-$file.log 2>&1 &