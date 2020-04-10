batch=100
idx0=$1
idx1=$2
gpu=$3
path_source=../data/poetry_small.json
nsamples=15
path_config=../web/demo_config/config_poem.json
i0=$idx0
while [ $i0 -le $idx1 ]
do
echo process $i0-$(( $i0 + $batch ))
#nohup python -u peomGenerator.py $path_source $path_config $i0 $(($i0+$batch)) $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1
i0=$(( $i0 + $batch ))
done
