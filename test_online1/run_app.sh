style=poem
port=6000
gpus=0
nohup python -u app.py $style $port $gpus >> log/gen-$style-$port-$gpus.log 2>&1 &

style=prose
port=6001
gpus=1
nohup python -u app.py $style $port $gpus >> log/genProse-$style-$port-$gpus.log 2>&1 &

style=gou
port=6002
gpus=2
nohup python -u app.py $style $port $gpus >> log/genGou-$style-$port-$gpus.log 2>&1 &