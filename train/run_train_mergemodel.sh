export CUDA_VISIBLE_DEVICES=3,1,2,0,4,5,6,7
nohup python -u train_mergemodel.py \
        --device=0,1,2,3,4,5,6,7 \
        --model_config=model/model_merged6/config.json \
        --tokenizer_path=model/model_merged6/vocab.txt \
        --tokenized_data_path0=../data1/userdata_mergedmodel/ \
        --tokenized_data_path1=../data1/godText_mergedmodel/ \
        --epochs=100 \
        --log_step=100 \
        --min_length=8 \
        --stride=64 \
        --max_steps_perEpoch_perPiece=1000 \
        --batch_size=64 \
        --pretrained_model=model/model_merged6/model_epoch44_step2540000_loss-2.40/ \
        --output_dir=model/model_merged6/ >> log/finetune-mergemodel6.log 2>&1 &