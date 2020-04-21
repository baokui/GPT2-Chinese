N=$1
maxPort=$2
name=$3
url0=http://10.160.22.73:
for((i=0;i<$N;i++))
do
ii=$[$i%$maxPort]
port=$[ii+5000]
nohup python -u test_post_online.py $port $url0 >> log/test-$name-$maxPort-$N.log 2>&1 &
done
#(10,10)

#(16,4) number of samles:10,total time:35.0058s, QPS:0.2857
#(20,4) number of samles:10,total time:43.0207s, QPS:0.2324
#(30,4) number of samles:10,total time:67.8125s, QPS:0.1697
#(50,4) number of samles:10,total time:95.3261s, QPS:0.1049
