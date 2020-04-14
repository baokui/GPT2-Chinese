import tensorflow as tf
import os
class ConvBlock(tf.keras.Model):
    """Convolutional Block consisting of (conv->bn->relu).
    Arguments:
      num_filters: number of filters passed to a convolutional layer.
      kernel_size: the size of convolution kernel
      weight_decay: weight decay
      dropout_rate: dropout rate.
    """
    def __init__(self, num_filters, kernel_size,
                 weight_decay=1e-4, dropout_rate=0.):
        super(ConvBlock, self).__init__()
        self.conv = tf.keras.layers.Conv2D(num_filters,
                                           kernel_size,
                                           padding="same",
                                           use_bias=False,
                                           kernel_initializer="he_normal",
                                           kernel_regularizer=tf.keras.regularizers.l2(weight_decay))
        self.bn = tf.keras.layers.BatchNormalization()
        self.dropout = tf.keras.layers.Dropout(dropout_rate)
    def call(self, x, training=True):
        output = self.conv(x)
        output = self.bn(x, training=training)
        output = tf.nn.relu(output)
        output = self.dropout(output, training=training)
        return output


def save_model_for_production(model, version='1', path='prod_models'):
    tf.keras.backend.set_learning_phase(1)
    if not os.path.exists(path):
        os.mkdir(path)
    export_path = os.path.join(
        tf.compat.as_bytes(path),
        tf.compat.as_bytes(version))
    builder = tf.compat.v1.saved_model.builder.SavedModelBuilder(export_path)
    model_input = tf.compat.v1.saved_model.build_tensor_info(model.input)
    model_output = tf.compat.v1.saved_model.build_tensor_info(model.output)
    prediction_signature = (
        tf.compat.v1.saved_model.signature_def_utils.build_signature_def(
            inputs={'inputs': model_input},
            outputs={'outputs': model_output},
            method_name=tf.compat.v1.saved_model.signature_constants.PREDICT_METHOD_NAME))
    with tf.compat.v1.keras.backend.get_session() as sess:
        builder.add_meta_graph_and_variables(
            sess=sess, tags=[tf.compat.v1.saved_model.tag_constants.SERVING],
            signature_def_map={
                'predict': prediction_signature,
                tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature
            })
        builder.save()
model = ConvBlock(32, 3, 1e-4, 0.5)
x = tf.ones((4, 224, 224, 3))
y = model(x)
print(model.layers)
