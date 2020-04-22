style=0
port=6000
gpus=0
nohup python -u app.py $style $port $gpus >> log/gou-$style-$port-$gpus.log 2>&1 &

style=1
port=6001
gpus=1
nohup python -u app.py $style $port $gpus >> log/gou-$style-$port-$gpus.log 2>&1 &

style=2
port=6002
gpus=2
nohup python -u app.py $style $port $gpus >> log/gou-$style-$port-$gpus.log 2>&1 &