mode=segment

for((idx0=0;idx0<1;idx0++))
do
for((idx1=0;idx1<10;idx1++))
do
file=00$idx0$idx1
path_source=../data/202002/$file
path_target=../data/202002_seg/$file.txt
nohup python -u sentsement.py $mode $path_source $path_target >> log/seg-$file.log 2>&1 &
done
done