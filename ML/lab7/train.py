# Tudor Berariu, 2015
import numpy as np                                  # Needed to work with arrays
from argparse import ArgumentParser

import matplotlib
matplotlib.use('TkAgg')
import pylab

from data_loader import load_mnist
from feed_forward import FeedForward
from transfer_functions import identity, logistic, hyperbolic_tangent

def eval_nn(nn, imgs, labels, maximum = 0):
    # TODO (4.b)
    # Compute the confusion matrix
    sum_mat= np.zeros((10, 1))
    confusion_matrix = np.zeros((10, 10))
    correct_no = 0
    how_many = imgs.shape[0] if maximum == 0 else maximum
    for i in range(imgs.shape[0])[:how_many]:
        y = np.argmax(nn.forward(imgs[i]))
        t = labels[i]
        if y == t:
            correct_no += 1
        confusion_matrix[y][t] += 1
        sum_mat[y] += 1
    for i in range(10):
        for j in range(10):
            confusion_matrix[i][j] /= sum_mat[y]
    return float(correct_no) / float(how_many), confusion_matrix

def train_nn(nn, data, args):
    pylab.ion()
    cnt = 0
    for i in np.random.permutation(data["train_no"]):

        cnt += 1

        # TODO (4.a)
        t_target = np.zeros((10, 1))
        t_target[data["train_labels"][i]] = 1
        inputs = data["train_imgs"][i]
        last_inputs = nn.forward(inputs)
        output_errors = last_inputs - t_target
        nn.backward(inputs, output_errors)
        nn.update_parameters(args.learning_rate) 

        # Evaluate the network
        if cnt % args.eval_every == 0:
            test_acc, test_cm = \
                eval_nn(nn, data["test_imgs"], data["test_labels"])
            train_acc, train_cm = \
                eval_nn(nn, data["train_imgs"], data["train_labels"], 5000)
            print("Train acc: %2.6f ; Test acc: %2.6f" % (train_acc, test_acc))
            pylab.imshow(test_cm)
            pylab.draw()

            matplotlib.pyplot.pause(0.001)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--learning_rate", type = float, default = 0.001,
                        help="Learning rate")
    parser.add_argument("--eval_every", type = int, default = 200,
                        help="Learning rate")
    args = parser.parse_args()


    mnist = load_mnist()
    input_size = mnist["train_imgs"][0].size
    print input_size
    nn = FeedForward(input_size, [(300, logistic), (10, identity)])
    print(nn.to_string())

    train_nn(nn, mnist, args)
