export CUDA_VISIBLE_DEVICES=3,1,2,0
nohup python -u train_douyin.py \
        --device=0,1,2,3 \
        --model_config=model/model_douyin/config.json \
        --tokenizer_path=model/model_douyin/vocab.txt \
        --tokenized_data_path=model/model_douyin/tokens/ \
        --epochs=100 \
        --log_step=100 \
        --min_length=8 \
        --stride=64 \
        --max_steps_perEpoch_perPiece=1000 \
        --batch_size=64 \
        --output_dir=model/model_douyin/ >> log/train_douyin.log 2>&1 &