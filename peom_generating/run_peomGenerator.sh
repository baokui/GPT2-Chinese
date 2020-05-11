mkdir log
mkdir data
path_source=data/poem_new_white.json
nsamples=20
path_config=../bin/config/config_poem.json


idx0=0
idx1=1300
gpu=0
nohup python -u poem_white_generate.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=1000
idx1=2000
gpu=1
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=2000
idx1=3000
gpu=2
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=3000
idx1=4000
gpu=3
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=4000
idx1=5000
gpu=0
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=5000
idx1=6000
gpu=1
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=6000
idx1=7000
gpu=2
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=70000
idx1=80000
gpu=7
#nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
