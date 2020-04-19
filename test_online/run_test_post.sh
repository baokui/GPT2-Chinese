N=$1
for((i=0;i<$N;i++))
do
nohup python -u test_post.py >> log/test-$N-$i.log 2>&1 &
done