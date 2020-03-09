filename=202001
for((i=0;i<9;i++))
do
name=000$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1 &
done
i=9
name=000$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1

for((i=0;i<9;i++))
do
name=001$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1 &
done
i=9
name=001$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1

for((i=0;i<9;i++))
do
name=002$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1 &
done
i=9
name=002$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1

for((i=1;i<9;i++))
do
name=003$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1 &
done
i=9
name=003$i
nohup python -u datapro.py ../data/$filename/$name $name >> log/$name.log 2>&1