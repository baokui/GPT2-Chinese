idx0=240000
idx1=280000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=280000
idx1=320000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=320000
idx1=360000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=360000
idx1=400000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=400000
idx1=440000
gpu=4
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=440000
idx1=480000
gpu=5
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=480000
idx1=520000
gpu=6
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=520000
idx1=560000
gpu=7
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
