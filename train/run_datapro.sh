path_vocab=model/model_merged6/vocab.txt
path_source=data1/godtext
path_target=data1/tokens_godtext
token_mask=[MASK_gou]
maxline=200000
mkdir path_target
nohup python -u $path_vocab $path_source $path_target/god $token_mask $maxline >> log/god-$hour.log 2>&1 &

t=1
for((Hour=0;Hour<24;Hour++))
do
if [ $Hour -lt 10 ];then
Hour=$((10#$Hour))
hour=0$Hour
else
hour=$Hour
fi
path_vocab=model/model_merged6/vocab.txt
path_source=data1/vpalog/$hour
path_target=data1/tokens_vpalog
token_mask=[MASK_gou]
maxline=200000
mkdir path_target
nohup python -u $path_vocab $path_source $path_target/vpa-$hour $token_mask $maxline >> log/vpa-$hour.log 2>&1 &
done