#tensorflow_version 2.x
import tensorflow as tf
print(tf.__version__)
from tensorflow.keras import *
import tensorflow as tf
from tensorflow.keras import models, layers, optimizers

## 样本数量
n = 800
## 生成测试用数据集
X = tf.random.uniform([n, 2], minval=-10, maxval=10)
w0 = tf.constant([[2.0], [-1.0]])
b0 = tf.constant(3.0)
Y = X @ w0 + b0 + tf.random.normal([n, 1],
                                   mean=0.0, stddev=2.0)  # @表示矩阵乘法,增加正态扰动
## 建立模型
tf.keras.backend.clear_session()
inputs = layers.Input(shape=(2,), name="inputs")  # 设置输入名字为inputs
outputs = layers.Dense(1, name="outputs")(inputs)  # 设置输出名字为outputs
linear = models.Model(inputs=inputs, outputs=outputs)
linear.summary()
## 使用fit方法进行训练
linear.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
linear.fit(X, Y, batch_size=8, epochs=100)
tf.print("w = ", linear.layers[1].kernel)
tf.print("b = ", linear.layers[1].bias)

## 将模型保存成pb格式文件
export_path = "./data/linear_model/"
version = "1"  # 后续可以通过版本号进行模型版本迭代与管理
linear.save(export_path + version, save_format="tf")