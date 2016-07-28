import sys
import getopt
import numpy as np

from parse import *

def main(argv):
    train_file = ""
    validation_file = ""

    try:
        opts, args = getopt.getopt(argv, "t:v:")
    except getopt.GetoptError, e:
        print e
        print 'kmeans.py -t <trainFile> -v <validationFile>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'kmeans.py -t <trainFile> -v <validationFile>'
            sys.exit(2)
        elif opt == '-t':
            train_file = arg
        elif opt == '-v':
            validation_file = arg

    if train_file == '':
        print 'kmeans.py -t <trainFile> -v <validationFile>'
        sys.exit(2)

    print 'Parsing training data...'
    parse = parse_generated_data(train_file)
    train_features, train_labels = parse.get_most_common_data()
    vectors = np.array(train_features)

    print 'Finding 5 means...'
    means, clusters = find_centers(np.array(vectors), 5)

    print 'Calculating results...'
    mean_labels = []
    for iter_mean in range(5):
        mean_labels.append([0 for counter in range(6)])

    for label, vector in zip(train_labels, vectors):
        bestmukey = min([(i[0], np.linalg.norm(vector - means[i[0]])) for i in enumerate(means)], key=lambda t:t[1])[0]
        mean_labels[bestmukey][label] = mean_labels[bestmukey][label] + 1

    print 'Training results...'
    print mean_labels

    if validation_file:
        print 'Parsing validation data...'
        parse = parse_generated_data(validation_file)
        valid_features, valid_labels = parse.get_most_common_data()
        vectors = np.array(valid_features)

        print 'Calculating results...'
        mean_labels = []
        for iter_mean in range(5):
            mean_labels.append([0 for counter in range(6)])

        for label, vector in zip(valid_labels, vectors):
            bestmukey = min([(i[0], np.linalg.norm(vector - means[i[0]])) for i in enumerate(means)], key=lambda t:t[1])[0]
            mean_labels[bestmukey][label] = mean_labels[bestmukey][label] + 1

        print 'Validation results...'
        print mean_labels

def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x-mu[i[0]])) for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]

    return clusters

def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))

    return newmu

def has_converged(mu, oldmu):
    return set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu])

def find_centers(X, K):
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    iter_count = 0

    while not has_converged(mu, oldmu):
        iter_count += 1
        print "Iteration " + str(iter_count)
        oldmu = mu
        clusters = cluster_points(X, mu)
        mu = reevaluate_centers(oldmu, clusters)

    return(mu, clusters)

if __name__ == "__main__":
    main(sys.argv[1:])
