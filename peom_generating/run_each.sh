batch=100
idx0=$1
idx1=$2
gpu=$3
echo $idx0 $idx1 $gpu
path_source=../data/poetry_small.json
nsamples=15
path_config=../web/demo_config/config_poem.json
i0=$idx0
while [ $i0 -lt $idx1 ]
do
i1=$(( $i0 + $batch ))
echo process $i0-$i1
nohup python -u peomGenerator.py $path_source $path_config $i0 $i1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1
i0=$i1
done
