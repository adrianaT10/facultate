# Tudor Berariu, 2015
import numpy as np                                  # Needed to work with arrays
from argparse import ArgumentParser
from copy import copy
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
import pylab
import time


from data_loader import load_cifar, load_cfk
from convolutional import ConvolutionalLayer
from feed_forward import FeedForward
from fully_connected import FcLayer
from max_pooling import MaxPoolingLayer
from linearize import LinearizeLayer, LinearizeLayerReverse
from relu import ReluLayer
from soft_max import SoftMaxLayer
from tanh import TanHLayer
from transfer_functions import hyperbolic_tangent, logistic, identity



def eval_nn(nn, imgs, labels, dim, maximum = 0):
    # Compute the confusion matrix
    confusion_matrix = np.zeros((dim, dim))
    correct_no = 0
    how_many = imgs.shape[0] if maximum == 0 else maximum
    for i in range(imgs.shape[0])[:how_many]:
        y = np.argmax(nn.forward(imgs[i]))
        t = labels[i]
        if y == t:
            correct_no += 1
        confusion_matrix[y][t] += 1

    return float(correct_no) / float(how_many), confusion_matrix / float(how_many)


def train_nn(nn, data, args, no_classes):
    pylab.ion()
    cnt = 0
    train_acc = 0
    test_acc = 0


    train_logf = open('train.log', 'w') 
    test_logf = open('test.log', 'w')

    while train_acc < 0.8 and test_acc < 0.8:

        for i in np.random.permutation(data["train_no"]):
            cnt += 1

            inputs = data["train_imgs"][i]
            label = data["train_labels"][i]

            targets = np.zeros((no_classes, 1))
            targets[label] = 1

            outputs = nn.forward(inputs)

            errors = copy(targets)
            errors[label] = -1 / outputs[label]

            # if cnt % 32 == 0:
            nn.backward(inputs, errors)
            nn.update_parameters(args.learning_rate, args.momentum)

            # # Evaluate the network
            if cnt % args.eval_every == 0:
                test_acc, test_cm = \
                    eval_nn(nn, data["test_imgs"], data["test_labels"], no_classes)
                train_acc, train_cm = \
                    eval_nn(nn, data["train_imgs"], data["train_labels"], no_classes, 5000)
                print("[" + time.asctime( time.localtime(time.time()) ) + "]Train acc: %2.6f ; Test acc: %2.6f episode %f" % (train_acc, test_acc, cnt))

                train_logf.write(str(cnt) + "," + str(train_acc) + "\n")
                train_logf.flush()
                test_logf.write(str(cnt) + "," + str(test_acc) + "\n")
                test_logf.flush()

                pylab.imshow(test_cm)
                pylab.draw()

                matplotlib.pyplot.pause(0.001)

    train_logf.close()
    test_logf.close()

        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--learning_rate", type = float, default = 0.001,
                        help="Learning rate")
    parser.add_argument("--eval_every", type = int, default = 1000,
                        help="Learning rate")
    parser.add_argument("--momentum", type = float, default = 0,
                        help="Learning rate")
    args = parser.parse_args()

    # nn = FeedForward([ConvolutionalLayer(3, 32, 32, 6, 5, 1), MaxPoolingLayer(2), ConvolutionalLayer(6, 14, 14, 16, 5, 1), MaxPoolingLayer(2), ConvolutionalLayer(16, 5, 5, 120, 5, 1), LinearizeLayer(120, 1, 1), FcLayer(120, 84, identity), FcLayer(84, 10, identity), SoftMaxLayer()])
    
    # CFK
    # data = load_cfk()
    # nn = FeedForward([LinearizeLayer(3, 32, 32), FcLayer(3072, 300, identity), TanHLayer(), FcLayer(300, 62, identity), SoftMaxLayer()])
    # nn = FeedForward([LinearizeLayer(3, 32, 32), FcLayer(3072, 300, identity), TanHLayer(), FcLayer(300, 100, identity), TanHLayer(), FcLayer(100, 62, identity), SoftMaxLayer()])
    # nn = FeedForward([LinearizeLayer(3, 32, 32), FcLayer(3072, 600, identity), TanHLayer(), FcLayer(600, 62, identity), SoftMaxLayer()])
    # train_nn(nn, data, args, 62)

    #CIFAR
    # data = load_cifar()
    # nn = FeedForward([LinearizeLayer(3, 32, 32), FcLayer(3072, 300, identity), TanHLayer(), FcLayer(300, 10, identity), SoftMaxLayer()])
    # nn = FeedForward([LinearizeLayer(3, 32, 32), FcLayer(3072, 600, identity), TanHLayer(), FcLayer(600, 400, identity), TanHLayer(), FcLayer(400, 100, identity), TanHLayer(), FcLayer(100, 10, identity), SoftMaxLayer()])
    # train_nn(nn, data, args, 10)

    #CONV CFK
    data = load_cfk()
    # nn = FeedForward([ConvolutionalLayer(3, 32, 32, 6, 5, 1), MaxPoolingLayer(2), ConvolutionalLayer(6, 14, 14, 16, 5, 1), MaxPoolingLayer(2), ConvolutionalLayer(16, 5, 5, 120, 5, 1), LinearizeLayer(120, 1, 1), FcLayer(120, 84, identity), FcLayer(84, 62, identity), SoftMaxLayer()])    
    # nn = FeedForward([ConvolutionalLayer(3, 32, 32, 6, 5, 1), MaxPoolingLayer(2), ReluLayer(), ConvolutionalLayer(6, 14, 14, 16, 5, 1), MaxPoolingLayer(2), ReluLayer(), LinearizeLayer(16, 5, 5), FcLayer(400, 300, identity), TanHLayer(), FcLayer(300, 62, identity), SoftMaxLayer()])
    # nn = FeedForward([ConvolutionalLayer(3, 32, 32, 6, 5, 1), MaxPoolingLayer(2), ReluLayer(), ConvolutionalLayer(6, 14, 14, 16, 5, 1), ReluLayer(), ConvolutionalLayer(16, 10, 10, 25, 3, 1), ReluLayer(),  ConvolutionalLayer(25, 8, 8, 40, 3, 1), ReluLayer(), MaxPoolingLayer(2), 
        # LinearizeLayer(40, 3, 3), FcLayer(360, 84, identity), TanHLayer(), FcLayer(84, 62, identity), SoftMaxLayer()])
    # nn = FeedForward([ConvolutionalLayer(3, 32, 32, 6, 5, 1), ReluLayer(), ConvolutionalLayer(6, 28, 28, 16, 5, 1), ReluLayer(), ConvolutionalLayer(16, 24, 24, 25, 3, 1), ReluLayer(),  ConvolutionalLayer(25, 22, 22, 40, 3, 1), ReluLayer(), MaxPoolingLayer(2), 
        # LinearizeLayer(40, 10, 10), FcLayer(4000, 1000, identity), ReluLayer(),  FcLayer(1000, 300, identity), ReluLayer(), FcLayer(300, 62, identity), SoftMaxLayer()])
    nn = FeedForward([ConvolutionalLayer(3, 32, 32, 20, 5, 1), ReluLayer(), ConvolutionalLayer(20, 28, 28, 20, 5, 1), ReluLayer(), ConvolutionalLayer(20, 24, 24, 50, 3, 1), ReluLayer(),  ConvolutionalLayer(50, 22, 22, 30, 3, 1), ReluLayer(), MaxPoolingLayer(2), 
        LinearizeLayer(30, 10, 10), FcLayer(3000, 1000, identity), ReluLayer(),  FcLayer(1000, 300, identity), ReluLayer(), FcLayer(300, 62, identity), SoftMaxLayer()])
    train_nn(nn, data, args, 62)

    # CONV CIFAR
    # data = load_cifar()
    # nn = FeedForward([ConvolutionalLayer(3, 32, 32, 20, 5, 1), MaxPoolingLayer(2), ConvolutionalLayer(20, 14, 14, 25, 5, 1), MaxPoolingLayer(2), ConvolutionalLayer(25, 5, 5, 100, 5, 1), LinearizeLayer(100, 1, 1), FcLayer(100, 84, identity), FcLayer(84, 10, identity), SoftMaxLayer()])
    # train_nn(nn, data, args, 10)