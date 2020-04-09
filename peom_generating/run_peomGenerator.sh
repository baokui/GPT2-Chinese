mkdir log
mkdir data
path_source=../data/poetry_small.json
nsamples=15
path_config=../web/demo_config/config_poem.json

idx0=160000
idx1=170000
gpu=0
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=170000
idx1=180000
gpu=1
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=180000
idx1=190000
gpu=2
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=190000
idx1=200000
gpu=3
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=200000
idx1=210000
gpu=4
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=210000
idx1=220000
gpu=5
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=220000
idx1=230000
gpu=6
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=230000
idx1=240000
gpu=7
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
