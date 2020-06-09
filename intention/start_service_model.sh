export CUDA_VISIBLE_DEVICES=3
port=1001
base_dir=data1
save_dir=checkpoints1/textrnn
nohup python -u service_model.py $port $base_dir $save_dir >> log/service-$port.log 2>&1 &