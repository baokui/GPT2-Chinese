N=$1
maxThread=1
url0=http://10.160.22.73:
port=5000
for((i=0;i<$N;i++))
do
nohup python -u test_post_online.py $port $url0 >> log/test-gou-$maxThread-$N.log 2>&1 &
done