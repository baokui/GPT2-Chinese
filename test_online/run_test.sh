path_source=data/test_parallel.txt
path_target=result/test_text-godTextPretrain.json
path_config=demo_config/config_godText_large1.json,demo_config/config_poem.json,demo_config/config_dabaigou.json
doPredict=1,1,1,1

gpus0=(0 1 2 3 4)
gpus1=(5)
gpus2=(6 7)
nb0=${#gpus0[@]}
nb1=${#gpus1[@]}
nb2=${#gpus2[@]}
for((i=0;i<10;i++))
do
idx=$i
path_target=result/test-$idx.json
g0=$(( $i % $nb0 ))
g1=$(( $i % $nb1 ))
g2=$(( $i % $nb2 ))
gpus=${gpus0[$g0]},${gpus1[$g1]},${gpus2[$g2]}
nohup python -u test.py $path_source $path_target $path_config $doPredict $gpus >> log/test_text-test-$idx.log 2>&1 &
done
