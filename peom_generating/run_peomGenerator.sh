mkdir log
mkdir data
path_source=../data/poetry_small.json
nsamples=15
path_config=../web/demo_config/config_poem.json

idx0=0
idx1=10000
gpu=0
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=10000
idx1=20000
gpu=1
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=20000
idx1=30000
gpu=2
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=30000
idx1=40000
gpu=3
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=40000
idx1=50000
gpu=4
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=50000
idx1=60000
gpu=5
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=60000
idx1=70000
gpu=6
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=70000
idx1=80000
gpu=7
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
