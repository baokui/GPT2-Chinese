for((i=1;i<10;i++))
do
name=000$i
nohup python -u datapro.py ../data/sogouInput/$name $name >> log/$name.log 2>&1 &
done