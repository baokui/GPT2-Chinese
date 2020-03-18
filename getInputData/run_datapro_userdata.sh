mode=char
path_data=../data/userdata
idx=00
name=$idx.txt
nohup python -u datapro_userdata.py $mode $path_data $idx $name >> log/datapro-userdata-$name.log 2>&1 &


for((j=0;j<4;j++))
do
for((i=0;i<9;i++))
do
name=00$j$i
nohup python -u datapro_dabaigou.py $mode ../data/$filename/$name.txt $name >> log/datapro-dabaigou-seg-$name.log 2>&1 &
done
i=9
name=00$j$i
nohup python -u datapro_dabaigou.py $mode ../data/$filename/$name.txt $name >> log/datapro-dabaigou-seg-$name.log
done
