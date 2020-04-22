N=$1
maxGPU=4
style=gou
for((i=0;i<$N;i++))
do
    port=$[i+2000]
    gpus=$[$i%$maxGPU]
    nohup python -u app.py $style $port $gpus >> log/gen-$style-$port-$gpus.log 2>&1 &
done