N=$1
style=$2
maxGPU=$3
for((i=0;i<$N;i++))
do
    port=$[i+2000]
    gpus=$[$i%$maxGPU]
    nohup python -u app.py $style $port $gpus >> log/gen-$style-$port-$gpus.log 2>&1 &
done

#sh run_app_batch.sh 20 gou 4