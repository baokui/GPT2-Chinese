export CUDA_VISIBLE_DEVICES=2,3,4,5,6,7
nohup python -u train_mergemodel.py \
        --device=0,1,2,3,4,5 \
        --model_config=model/model_merged6_finetune/config.json \
        --tokenizer_path=model/model_merged6_finetune/vocab.txt \
        --tokenized_data_path0=./data1/tokens_vpalog/ \
        --tokenized_data_path1=./data/godText_mergedmodel/ \
        --epochs=100 \
        --log_step=100 \
        --min_length=8 \
        --stride=64 \
        --max_steps_perEpoch_perPiece=1000 \
        --batch_size=96 \
        --pretrained_model=model/model_merged6_finetune/pretrained/ \
        --output_dir=model/model_merged6_finetune/ >> log/mergemodel6_finetune.log 2>&1 &