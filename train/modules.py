import json
import os
import torch
def model_reshape(path_source,path_target):
    config0 = json.load(open(os.path.join(path_source,'config.json'),'r'))
    n_ctx0 = config0['n_ctx']
    config1 = json.load(open(os.path.join(path_target, 'config.json'),'r'))
    n_ctx1 = config1['n_ctx']
    D = torch.load(os.path.join(path_source,"pytorch_model.bin"))
    if n_ctx1>n_ctx0:
        print('invalid n_ctx')
        return
    if n_ctx1==n_ctx0:
        torch.save(D,os.path.join(path_target,"pytorch_model.bin"))
        return
    D1 = {}
    for k in D:
        if k=="transformer.wpe.weight":
            D1[k] = D[k][:n_ctx1,:]
        elif "transformer.h." in k and ".attn.bias" in k:
            D1[k] = D[k][:,:,:n_ctx1,:n_ctx1]
        else:
            D1[k] = D[k]
    torch.save(D1, os.path.join(path_target, "pytorch_model.bin"))