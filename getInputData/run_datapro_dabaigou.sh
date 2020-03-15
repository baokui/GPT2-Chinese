mode=word
filename=202002_seg
for((j=0;j<4;j++))
do
for((i=0;i<9;i++))
do
name=00$j$i
nohup python -u datapro_dabaigou.py $mode ../data/$filename/$name.txt $name >> log/$name.log 2>&1 &
done
i=9
name=00$j$i
nohup python -u datapro_dabaigou.py $mode ../data/$filename/$name.txt $name >> log/$name.log
done
