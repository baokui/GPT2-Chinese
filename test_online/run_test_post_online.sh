iN=$1
maxPort=$2
name=$3
url0=http://10.160.22.73:
for((i=0;i<$N;i++))
do
ii=$[$i%$maxPort]
port=$[ii+5000]
nohup python -u test_post.py $port $url0 >> log/test-$name-$maxPort-$N.log 2>&1 &
done