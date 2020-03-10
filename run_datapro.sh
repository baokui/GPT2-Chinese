nohup python -u datapro.py \
        --model_config=model/gpt2_prose/config.json \
        --tokenizer_path=model/gpt2_prose/vocab.txt \
        --raw_data_path=data/data_multiReplace_all.json \
        --tokenized_data_path=data/data_multiReplace_all_tokenized/ \
        --num_pieces=100 \
        --min_length=10 \
        >> log/datapro_multiReplace_all.log 2>&1 &