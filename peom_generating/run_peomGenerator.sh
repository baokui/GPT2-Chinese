mkdir log
mkdir data
path_source=/search/odin/guobk/vpa/GPT2-Chinese/data/poetry_small.json
nsamples=15
path_config=../web/demo_config/config_poem.json
idx0=0
idx1=10000
gpu=0
nohup python -u peomGenerator.py $path_source $path_config $idx0 $idx1 $gpu $nsamples >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

