docker run -t --rm -p 8701:8701 \
    -v "/Users/.../data/linear_model/" \
    -e MODEL_NAME=linear_model \
    tensorflow/serving & >server.log 2>&1

curl -d '{"instances": [1.0, 2.0, 5.0]}' \
    -X POST https://localhost:8701/v1/models/linear_model:predict
{
    "predictions": [[3.06546211], [5.01313448]
    ]
}

source=/search/odin/guobk/vpa/GPT2-Chinese/test_tfserving/data/linear_model/
model=export_model
target=/models/$model
docker run -p 8702:8702 --mount type=bind,source=$source,target=$target -e MODEL_NAME=$model -t tensorflow/serving &

docker run -dt -p 8704:8704 -v /search/odin/guobk/vpa/GPT2-Chinese/test_tfserving/data/linear_model/:/models/export_model -e MODEL_NAME=export_model tensorflow/serving &


curl -d '{"instances": [1.0, 2.0, 5.0]}' -X POST http://localhost:8702/v1/models/$model:predict
curl -d '{"instances":[1.0, 2.0, 5.0]}' -X POST https://localhost:8704/v1/models/export_model:serving_default
