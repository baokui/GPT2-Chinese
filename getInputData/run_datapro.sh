sleep 3h
for((i=1;i<9;i++))
do
name=001$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1 &
done
i=9
name=001$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1

for((i=1;i<9;i++))
do
name=002$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1 &
done
i=9
name=002$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1

for((i=1;i<9;i++))
do
name=003$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1 &
done
i=9
name=003$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1