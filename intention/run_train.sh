mkdir log
base_dir="data2"
save_dir="checkpoints2/textrnn"
ckpt_dir="checkpoints1/textrnn"
nohup python -u train_model.py $base_dir $save_dir $ckpt_dir >> log/train.log 2>&1 &
nohup python -u train_model.py $base_dir $save_dir $save_dir predict >> log/test.log 2>&1 &