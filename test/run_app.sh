port=$1
nohup python -u app.py $port >> log/$port.log 2>&1 &