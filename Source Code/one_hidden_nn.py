import tensorflow.python.platform

import numpy as np
import tensorflow as tf

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
tf.app.flags.DEFINE_float('learning_rate', 0.001,
                            'The rate for the model to learn at in AdamOptimizer')
FLAGS = tf.app.flags.FLAGS

def generate_data(test_train_file, validation_file):
    print 'Getting and splitting test train data...'

    parse = parse_generated_data(test_train_file)
    x_train, y_train, x_test, y_test = parse.test_train_split_data(0.2)

    x_train = np.matrix(x_train).astype(np.float32)
    x_test = np.matrix(x_test).astype(np.float32)
    y_train = np.array(y_train).astype(dtype=np.uint8)
    y_train = (np.arange(NUM_LABELS) == y_train[:, None]).astype(np.float32)
    y_test = np.array(y_test).astype(dtype=np.uint8)
    y_test = (np.arange(NUM_LABELS) == y_test[:, None]).astype(np.float32)

    print 'Completed test train data...'
    print 'Getting validation data...'

    parse = parse_generated_data(validation_file)
    x_valid, y_valid = parse.get_data()

    x_valid = np.matrix(x_valid).astype(np.float32)
    y_valid = np.array(y_valid).astype(dtype=np.uint8)
    y_valid = (np.arange(NUM_LABELS) == y_valid[:, None]).astype(np.float32)

    return x_train, y_train, x_test, y_test, x_valid, y_valid

def create_model(x, dimensions):
    weights = create_weights(dimensions, 'xavier')
    biases = create_biases(dimensions, 'zeros')

    hidden = tf.add(tf.matmul(x, weights['hidden']), biases['hidden'])
    hidden = tf.nn.softmax(hidden)

    output = tf.add(tf.matmul(hidden, weights['output']), biases['output'])
    output = tf.nn.softmax(output)

    return output

def create_weights(dimensions, method):
    return {
        'hidden': create_matrix_distribution(dimensions['num_input'], dimensions['num_hidden'], method),
        'output': create_matrix_distribution(dimensions['num_hidden'], dimensions['num_output'], method)
    }

def create_biases(dimensions, method):
    return {
        'hidden': create_matrix_distribution(1, dimensions['num_hidden'], method),
        'output': create_matrix_distribution(1, dimensions['num_output'], method)
    }

def create_matrix_distribution(num_in, num_out, method='xavier'):
    if method == 'zeros':
        return tf.Variable(tf.zeros([num_in, num_out], dtype=tf.float32))
    elif method == 'uniform':
        return tf.Variable(tf.random_normal([num_in, num_out], dtype=tf.float32))
    else:
        low = -4 * np.sqrt(6.0 / (num_in + num_out))
        high = 4 * np.sqrt(6.0 / (num_in + num_out))
        return tf.Variable(tf.random_uniform([num_in, num_out], minval=low, maxval=high, dtype=tf.float32))

def main(argv=None):
    verbose = FLAGS.verbose
    test_train_file = FLAGS.test_train
    validation_file = FLAGS.validation
    num_epochs = FLAGS.num_epochs
    num_hidden = FLAGS.num_hidden
    learning_rate = FLAGS.learning_rate

    x_train, y_train, x_test, y_test, x_valid, y_valid = generate_data(test_train_file, validation_file)

    # Get the shape of the training data.
    train_size,num_features = x_train.shape

    # This is where training samples and labels are fed to the graph.
    # These placeholder nodes will be fed a batch of training data at each
    # training step using the {feed_dict} argument to the Run() call below.
    x = tf.placeholder("float", shape=[None, num_features])
    y = tf.placeholder("float", shape=[None, NUM_LABELS])

    # For the test data, hold the entire dataset in one constant node.
    test_data_node = tf.constant(x_test)

    # Define and initialize the network.
    dimensions = {
        'num_input': num_features,
        'num_hidden': num_hidden,
        'num_output': NUM_LABELS
    }
    model = create_model(x, dimensions)

    # Optimization.
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(model, y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Evaluation.
    correct_prediction = tf.equal(tf.argmax(model,1), tf.argmax(y,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    # Create a local session to run this computation.
    with tf.Session() as sess:
        # Run all the initializers to prepare the trainable parameters.
    	tf.initialize_all_variables().run()
    	if verbose:
    	    print 'Initialized!'
    	    print
    	    print 'Training.'

    	# Iterate and train.
    	for step in xrange(num_epochs * train_size // BATCH_SIZE):
    	    if verbose:
    	        print step,

    	    offset = (step * BATCH_SIZE) % train_size
    	    batch_data = x_train[offset:(offset + BATCH_SIZE), :]
    	    batch_labels = y_train[offset:(offset + BATCH_SIZE)]
    	    sess.run([optimizer, cost], feed_dict={x: batch_data, y: batch_labels})

    	print "Testing Accuracy:", accuracy.eval(feed_dict={x: x_test, y: y_test})
        print "Validation Accuracy:", accuracy.eval(feed_dict={x: x_valid, y: y_valid})

if __name__ == '__main__':
    tf.app.run()




