idx0=0
idx1=10000
gpu=0
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=10000
idx1=20000
gpu=1
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=20000
idx1=30000
gpu=2
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=30000
idx1=40000
gpu=3
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=40000
idx1=50000
gpu=4
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=50000
idx1=60000
gpu=5
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=60000
idx1=70000
gpu=6
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &

idx0=70000
idx1=80000
gpu=7
nohup sh run_each.sh $idx0 $idx1 $gpu >> ./log/poemGen-$idx0-$idx1.log 2>&1 &
