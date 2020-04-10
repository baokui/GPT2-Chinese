idx0=160000
idx1=170000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=170000
idx1=180000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=180000
idx1=190000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=190000
idx1=200000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=200000
idx1=210000
gpu=4
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=210000
idx1=220000
gpu=5
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=220000
idx1=230000
gpu=6
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=230000
idx1=240000
gpu=7
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
