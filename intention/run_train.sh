mkdir log
base_dir="data3"
save_dir="checkpoints3/textrnn"
ckpt_dir="checkpoints2/textrnn"
nohup python -u train_model.py $base_dir $save_dir $ckpt_dir >> log/train.log 2>&1 &
base_dir="data3"
save_dir="checkpoints3/textrnn"
ckpt_dir="checkpoints3/textrnn"
nohup python -u train_model.py $base_dir $save_dir $save_dir predict >> log/test-3.log 2>&1 &