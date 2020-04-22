port=$1
nohup python -u app_prose.py $port >> log/gou-$port.log 2>&1 &