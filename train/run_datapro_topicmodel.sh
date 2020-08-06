path_vocab=model/model_merged6/vocab.txt
path_source=data1/godtext_topic/
path_target=data1/tokens_godtext_topic
token_mask=[MASK]
maxline=200000
mkdir $path_target
nohup python -u datapro_topicmodel.py $path_vocab $path_source $path_target/god $token_mask $maxline >> log/god-topic.log 2>&1 &