import functools
import sets
import numpy as np
import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
import numpy as np

from parse import *

# Global variables.
NUM_LABELS = 2    # The number of labels.
BATCH_SIZE = 100  # The number of training examples to use per training step.

tf.app.flags.DEFINE_boolean('verbose', False,
                            'To verbosify or not.')
tf.app.flags.DEFINE_string('test_train', None,
                           'File containing the test/train data.')
tf.app.flags.DEFINE_string('validation', None,
                            'File containing the validation data.')
tf.app.flags.DEFINE_integer('num_epochs', 1,
                            'Number of passes over the training data.')
tf.app.flags.DEFINE_integer('num_hidden', 1,
                            'Number of nodes in the hidden layer.')
tf.app.flags.DEFINE_integer('num_layers', 1,
                            'Number of layers in the recurrent network')
tf.app.flags.DEFINE_float('dropout', 0.5,
                            'The dropout rate for the recurrent network')
tf.app.flags.DEFINE_float('learning_rate', 0.001,
                            'The rate for the model to learn at in AdamOptimizer')
FLAGS = tf.app.flags.FLAGS

def generate_data(test_train_file, validation_file):
    print 'Getting and splitting test train data...'

    parse = parse_generated_varying_data(test_train_file)
    x_train, y_train, x_test, y_test = parse.test_train_split_data(0.2)

    x_train = np.array(x_train).astype(np.float32)
    x_test = np.array(x_test).astype(np.float32)
    y_train = np.array(y_train).astype(dtype=np.uint8)
    y_train = (np.arange(NUM_LABELS) == y_train[:, None]).astype(np.float32)
    y_test = np.array(y_test).astype(dtype=np.uint8)
    y_test = (np.arange(NUM_LABELS) == y_test[:, None]).astype(np.float32)

    print 'Completed test train data...'
    print 'Getting validation data...'

    parse = parse_generated_varying_data(validation_file)
    x_valid, y_valid = parse.get_data()

    x_valid = np.array(x_valid).astype(np.float32)
    y_valid = np.array(y_valid).astype(dtype=np.uint8)
    y_valid = (np.arange(NUM_LABELS) == y_valid[:, None]).astype(np.float32)

    return x_train, y_train, x_test, y_test, x_valid, y_valid

def lazy_property(function):
    attribute = '_' + function.__name__

    @property
    @functools.wraps(function)
    def wrapper(self):
        if not hasattr(self, attribute):
            setattr(self, attribute, function(self))
        return getattr(self, attribute)
    return wrapper


class SequenceClassification:

    def __init__(self, data, target, dropout, num_hidden=200, num_layers=3):
        self.data = data
        self.target = target
        self.dropout = dropout
        self._num_hidden = num_hidden
        self._num_layers = num_layers
        self.prediction
        self.error
        self.optimize

    @lazy_property
    def prediction(self):
        # Recurrent network.
        network = rnn_cell.GRUCell(self._num_hidden)
        network = rnn_cell.DropoutWrapper(
            network, output_keep_prob=self.dropout)
        network = rnn_cell.MultiRNNCell([network] * self._num_layers)
        output, _ = rnn.dynamic_rnn(network, self.data, dtype=tf.float32)
        # Select last output.
        output = tf.transpose(output, [1, 0, 2])
        last = tf.gather(output, int(output.get_shape()[0]) - 1)
        # Softmax layer.
        weight, bias = self._weight_and_bias(
            self._num_hidden, int(self.target.get_shape()[1]))
        prediction = tf.nn.softmax(tf.matmul(last, weight) + bias)
        return prediction

    @lazy_property
    def cost(self):
        cross_entropy = -tf.reduce_sum(self.target * tf.log(self.prediction))
        return cross_entropy

    @lazy_property
    def optimize(self):
        learning_rate = 0.003
        optimizer = tf.train.RMSPropOptimizer(learning_rate)
        return optimizer.minimize(self.cost)

    @lazy_property
    def error(self):
        mistakes = tf.not_equal(
            tf.argmax(self.target, 1), tf.argmax(self.prediction, 1))
        return tf.reduce_mean(tf.cast(mistakes, tf.float32))

    @lazy_property
    def accuracy(self):
        correct_prediction = tf.equal(tf.argmax(self.prediction,1), tf.argmax(self.target, 1))
        return tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    @staticmethod
    def _weight_and_bias(in_size, out_size):
        weight = tf.truncated_normal([in_size, out_size], stddev=0.01)
        bias = tf.constant(0.1, shape=[out_size])
        return tf.Variable(weight), tf.Variable(bias)

def main(argv=None):
    verbose = FLAGS.verbose
    test_train_file = FLAGS.test_train
    validation_file = FLAGS.validation
    num_epochs = FLAGS.num_epochs
    num_hidden = FLAGS.num_hidden
    num_layers = FLAGS.num_layers
    dropout_rate = FLAGS.dropout
    learning_rate = FLAGS.learning_rate

    x_train, y_train, x_test, y_test, x_valid, y_valid = generate_data(test_train_file, validation_file)

    # Get the shape of the training data.
    train_size,num_steps,num_features = x_train.shape

    data = tf.placeholder(tf.float32, [None, num_steps, num_features])
    target = tf.placeholder(tf.float32, [None, NUM_LABELS])
    dropout = tf.placeholder(tf.float32)
    model = SequenceClassification(data, target, dropout, num_hidden, num_layers)
    sess = tf.Session()
    sess.run(tf.initialize_all_variables())

    for step in xrange(num_epochs * train_size // BATCH_SIZE):
        offset = (step * BATCH_SIZE) % train_size
        batch_data = x_train[offset:(offset + BATCH_SIZE), :]
        batch_labels = y_train[offset:(offset + BATCH_SIZE)]
        sess.run(model.optimize, {
            data: batch_data, target: batch_labels, dropout: dropout_rate})
        error = sess.run(model.error, {
        data: x_test, target: y_test, dropout: 1})
        print('Batch {:2d} error {:3.1f}%'.format(step + 1, 100 * error))

    test_accuracy = sess.run(model.accuracy, {data: x_test, target: y_test, dropout: 1})
    print 'Testing Accuracy:', test_accuracy
    validation_accuracy = sess.run(model.accuracy, {data: x_valid, target: y_valid, dropout: 1})
    print 'Validation Accuracy:', validation_accuracy

if __name__ == '__main__':
    tf.app.run()




