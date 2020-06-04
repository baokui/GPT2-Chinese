export CUDA_VISIBLE_DEVICES=3,1,2,0
nohup python -u train_mergemodel.py \
        --device=0,1,2,3 \
        --model_config=model/model_merged/config.json \
        --tokenizer_path=model/model_merged/vocab.txt \
        --tokenized_data_path0=../data/userdata_mergedmodel/ \
        --tokenized_data_path1=../data/godText_mergedmodel/ \
        --epochs=100 \
        --log_step=100 \
        --min_length=8 \
        --stride=64 \
        --max_steps_perEpoch_perPiece=1000 \
        --batch_size=64 \
        --pretrained_model=model/model_merged/model_epoch1_step50000_loss-2.74/ \
        --output_dir=model/model_merged/ >> log/train-mergemodel3.log 2>&1 &