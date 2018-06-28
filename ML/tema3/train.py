import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import pylab

from autoencoder import Autoencoder
from data_loader import load_mnist
from fully_connected import FullyConnected
from transfer_functions import identity, logistic, hyperbolic_tangent

def construct_nn(no_layers, layer_neurons, functions, input_size):
    funs = []
    for f in functions:
        if f == 0:
            faux = identity
        elif f == 1:
            faux = logistic
        else:
            faux = hyperbolic_tangent
        funs.append(faux)

    layers = []
    layers.append(FullyConnected(input_size, layer_neurons[0], funs[0]))

    for i in range(1, no_layers):
        layers.append(FullyConnected(layer_neurons[i - 1], layer_neurons[i], funs[i]))
 
    layers.append(FullyConnected(layer_neurons[no_layers - 1], input_size, funs[no_layers - 1]))

    return Autoencoder(layers)

# Trein the encoder for the genetic alg
def train_autoencoder(nn, data):
    learning_rate = 0.001
    momentum = 0

    cnt = 0
    for i in data["genetic_train_i"]:

        cnt += 1

        inputs = data["train_imgs"][i]
        targets = data["train_imgs"][i]

        outputs = nn.forward(inputs)
        errors = outputs - targets
        nn.backward(inputs, errors)
        nn.update_parameters(learning_rate, momentum)

# Train the classifier for the genetic alg
def train_classifier(nn, data):
    learning_rate = 0.001
    momentum = 0

    classifier = FullyConnected(nn.coding_size(), 10, logistic)

    cnt = 0
    for i in data["genetic_train_i"]:

        cnt += 1

        inputs = data["train_imgs"][i]
        label = data["train_labels"][i]
        targets = np.zeros((10, 1))
        targets[label] = 1

        coding = nn.code(inputs)
        outputs = classifier.forward(coding)

        errors = outputs - targets
        classifier.backward(coding, errors)
        classifier.update_parameters(learning_rate, momentum)

    badly_classified = 0

    for i in range(data["test_no"]):
        inputs = data["train_imgs"][i]
        label = data["train_labels"][i]

        coding = nn.code(inputs)
        outputs = classifier.forward(coding)

        y = np.argmax(outputs)
        if y != label:
            badly_classified += 1

    return badly_classified


def eval_nn(encoder, classifier, imgs, labels, maximum = 0):
    # Compute the confusion matrix
    confusion_matrix = np.zeros((10, 10))
    correct_no = 0
    how_many = imgs.shape[0] if maximum == 0 else maximum
    for i in range(imgs.shape[0])[:how_many]:
        coding = encoder.code(imgs[i])
        y = np.argmax(classifier.forward(coding))
        t = labels[i]
        if y == t:
            correct_no += 1
        confusion_matrix[y][t] += 1

    return float(correct_no) / float(how_many), confusion_matrix / float(how_many)

# Final Train
def train(nn, data):
    pylab.ion()
    learning_rate = 0.001
    momentum = 0

    for i in np.random.permutation(data["train_no"]):

        inputs = data["train_imgs"][i]
        targets = data["train_imgs"][i]

        outputs = nn.forward(inputs)
        errors = outputs - targets
        nn.backward(inputs, errors)
        nn.update_parameters(learning_rate, momentum)

    classifier = FullyConnected(nn.coding_size(), 10, logistic)

    cnt = 0
    for i in np.random.permutation(data["train_no"]):

        cnt += 1

        inputs = data["train_imgs"][i]
        label = data["train_labels"][i]
        targets = np.zeros((10, 1))
        targets[label] = 1

        coding = nn.code(inputs)
        outputs = classifier.forward(coding)

        errors = outputs - targets
        classifier.backward(coding, errors)
        classifier.update_parameters(learning_rate, momentum)  
        
        # # Evaluate the network
        if cnt % 2000 == 0:
            test_acc, test_cm = \
                eval_nn(nn, classifier, data["test_imgs"], data["test_labels"])
            train_acc, train_cm = \
                eval_nn(nn, classifier, data["train_imgs"], data["train_labels"], 5000)
            print("Train acc: %2.6f ; Test acc: %2.6f episode %f" % (train_acc, test_acc, cnt))

            pylab.imshow(test_cm)
            pylab.draw()

            matplotlib.pyplot.pause(0.001)

    rows_no, cols_no = (10, 10)
    full_img = np.zeros((0, 28 * cols_no))                  # prepare full image
    labels = np.zeros((rows_no, cols_no), dtype=int)
    for row_no in range(rows_no):
        row = np.zeros((28, 0))
        for col_no in range(cols_no):
            idx = np.random.randint(data["test_imgs"].shape[0])
            labels[(row_no, col_no)] = data["test_labels"][idx]

            row = np.hstack((row, nn.forward(data["test_imgs"][idx]).reshape(28, 28)))
        full_img = np.vstack((full_img, row))

    print(labels)
    pylab.imshow(full_img, cmap="Greys_r")
    pylab.show()

    matplotlib.pyplot.pause(500)



def read_config():
    f = open("config", "r")
    no_layers = int(f.readline())

    line = f.readline()
    line = line.split(" ")
    print line
    layers = [int(x) for x in line[:-1]]

    line = f.readline()
    line = line.split(" ")
    functions = [int(x) for x in line[:-1]]

    f.close()

    return no_layers, layers, functions



def main():
    data = load_mnist()
    no_layers, layers, functions = read_config()
    nn = construct_nn(no_layers, layers, functions, data["train_imgs"][0].size)
    train(nn, data)

if __name__ == "__main__":
    main()


