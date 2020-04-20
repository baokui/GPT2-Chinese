N=$1
maxPort=$2
name=$3
for((i=0;i<$N;i++))
do
ii=$[$i%$maxPort]
port=$[ii+5000]
nohup python -u test_post.py $port >> log/test-$name-$maxPort-$N.log 2>&1 &
done