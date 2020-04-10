idx0=80000
idx1=90000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=90000
idx1=100000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=100000
idx1=110000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=110000
idx1=120000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=120000
idx1=130000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=130000
idx1=140000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=150000
idx1=160000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=160000
idx1=170000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
