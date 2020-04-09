mkdir log
mkdir data
path_source=../data/poetry_small.json
nsamples=15
path_config=../web/demo_config/config_poem.json

idx0=80000
idx1=90000
gpu=0
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=90000
idx1=100000
gpu=1
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=100000
idx1=110000
gpu=2
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=110000
idx1=120000
gpu=3
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=120000
idx1=130000
gpu=0
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=130000
idx1=140000
gpu=1
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=140000
idx1=150000
gpu=2
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=150000
idx1=160000
gpu=3
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
