mode=segment

file=0000
path_source=data/202002/$file
path_source=data/202002_seg/$file.txt
nohup python -u sentsement.py $mode $path_source $path_target >> log/seg-$file.log 2>&1 &