N=$1
for((i=0;i<$N;i++))
do
ii=$[$i%10]
port=$[ii+5000]
nohup python -u test_post.py $port >> log/test-$N-$port.log 2>&1 &
done