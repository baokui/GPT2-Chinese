port=$1
nohup python -u app_gou $port >> log/gou-$port.log 2>&1 &