idx0=560000
idx1=570000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=570000
idx1=580000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=580000
idx1=590000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=590000
idx1=600000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=600000
idx1=610000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=610000
idx1=620000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=620000
idx1=630000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=630000
idx1=640000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
