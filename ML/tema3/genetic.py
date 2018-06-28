from argparse import ArgumentParser
from random import randint, random
import operator
from copy import deepcopy, copy
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import pylab

from data_loader import load_mnist
from train import construct_nn, train_autoencoder, train_classifier

MAX_ITERATIONS = 100
MUTATION_PROB = 0.1

# Convert from bit array to base 10 number
def get_number(bitlist):
    x = 0
    bitlist.reverse()
    k = 0
    for i in bitlist:
        x += pow(2, k) * i
        k += 1
    return x

# Get the characterstics of the net from the individual
def decode_nn(elem, args):
    no_layers = 0
    layers = []
    functions = []

    for i in range(args.max_layers):
        x = get_number(elem[i*args.max_neuron_bits : (i + 1) * args.max_neuron_bits])
        if x != 0:
            layers.append(x)
            no_layers += 1
            functions.append(elem[-args.max_layers + i])

    if no_layers == 0:
        return 0, [], []

    no_layers = no_layers * 2 - 1

    # make the net symetric
    fcopy = copy(functions)
    fcopy.reverse()
    functions += fcopy[1:]

    lcopy = copy(layers)
    lcopy.reverse()
    layers += lcopy[1:]

    return no_layers, layers, functions


# Generate the initial population
def generate_population(args):
    population = []
    dim =  args.max_neuron_bits * args.max_layers

    for i in range(args.pop_size):
        individual = []
        for j in range(dim):
            individual.append(randint(0, 1))
        for j in range(args.max_layers):
            individual.append(randint(0,2))
        population.append(individual)

    return population


# Select parent - tournament selection
def select_parents(sorted_population):
    indexes = []
    for i in range(5):
        indexes.append(randint(0, len(sorted_population) - 1))
    indexes.sort()
    return sorted_population[indexes[0]][0], sorted_population[indexes[1]][0]


# Apply crossover and get 2 children
def crossover(parent1, parent2, args):
    # one crossover point for the number of neurons per layer
    point1 = args.max_layers * args.max_neuron_bits
    index = randint(0, point1 - 1)
    child1 = copy(parent1[: index] + parent2[index : point1])
    child2 = copy(parent2[: index] + parent1[index : point1])

    # one crossover point for the functions used
    index = randint(point1, len(parent1)- 1)
    child1 += copy(parent1[point1 : index] + parent2[index :])
    child2 += copy(parent2[point1 : index] + parent1[index :])

    return child1, child2

# Apply mutation 
def mutation(x, args):
    for i in range(args.max_layers * args.max_neuron_bits):
        r = random()
        if r <= MUTATION_PROB:
            x[i] = 1 - x[i]

    for i in range(args.max_layers * args.max_neuron_bits, len(x)):
        r = random()
        if r <= MUTATION_PROB:
            x[i] = (x[i] + 1) % 3

    return x

# Train elem and compute the fitness
def fitness(elem, args, data):
    no_layers, layers, functions = decode_nn(elem, args)
    if no_layers == 0:
        return 9999
    encoder = construct_nn(no_layers, layers, functions, data["train_imgs"][0].size)

    train_autoencoder(encoder, data)

    errors = train_classifier(encoder, data)

    # number of badly classified examples + number of neurons on the middle layer
    return abs(errors + encoder.coding_size())


# Compute fitness for the population
def evaluate_population(population, args, data):
    fitness_by_elem = []
    for p in population:
        fit = fitness(p, args, data)
        fitness_by_elem.append((p, fit))

    return fitness_by_elem

# Sort population by its fitness
def sort_population(population_with_fitness):
    return sorted(population_with_fitness, key=operator.itemgetter(1))


def genetic(args, data):
    # indexes of pictures to be shown
    sample_indexes = np.zeros((10, 10))
    for i in range(10):
        for j in range(10):
            sample_indexes[i][j] = np.random.randint(data["test_no"])
    logf = open("log", "w")

    # initiate population and compute fitness
    population = generate_population(args)
    population_with_fitness = evaluate_population(population, args, data)
    sorted_population = sort_population(population_with_fitness)

    iteration = 0
    while iteration < MAX_ITERATIONS:
        print ""
        print "Iteration " + str(iteration)

        print_population(sorted_population, args)
        print_best(sorted_population[0], args, data, iteration, sample_indexes, logf)

        elite_no = 15 * args.pop_size / 100
        mates_no = (args.pop_size - elite_no) / 2

        new_population = []

        # select parents and create children
        for i in range(mates_no):
            parent1, parent2 = select_parents(sorted_population)
            child1, child2 = crossover(parent1, parent2, args)
            child1 = mutation(child1, args)
            child2 = mutation(child2, args)

            new_population.append(child1)
            new_population.append(child2)

        population_with_fitness = evaluate_population(new_population, args, data)
        # add the elite from the previous generation
        population_with_fitness += sorted_population[:elite_no]

        sorted_population = sort_population(population_with_fitness)

        iteration += 1

    best = sorted_population[0][0]
    no_layers, layers, functions = decode_nn(best, args)
    print "BEST LAYERS: " + str(no_layers) + " NEURONS: " + str(layers) + " FUNCTIONS: " + str(functions)

    return best

# Print the accuracy of the best individual and reconstruct images
def print_best(elem, args, data, iteration, sample_indexes, logf):
    no_layers, layers, functions = decode_nn(elem[0], args)
    if no_layers == 0:
        return 9999
    encoder = construct_nn(no_layers, layers, functions, data["train_imgs"][0].size)

    train_autoencoder(encoder, data)

    acc = 1.0 - (elem[1] - encoder.coding_size()) / float(data["test_no"])
    logf.write(str(iteration) + " " + str(acc) + "\n")
    print "BEST ACCURACY: " + str(acc)

    rows_no, cols_no = (10, 10)
    full_img = np.zeros((0, 28 * cols_no))                  # prepare full image
    labels = np.zeros((rows_no, cols_no), dtype=int)
    for row_no in range(rows_no):
        row = np.zeros((28, 0))
        for col_no in range(cols_no):
            idx = int(sample_indexes[row_no][col_no])
            labels[(row_no, col_no)] = data["test_labels"][idx]

            row = np.hstack((row, encoder.forward(data["test_imgs"][idx]).reshape(28, 28)))
        full_img = np.vstack((full_img, row))

    #print(labels)
    pylab.imshow(full_img, cmap="Greys_r")
    pylab.savefig('sample' + str(iteration) + '.png', bbox_inches='tight')
    

def print_population(population, args):
    for p in population:
        no_layers, layers, functions = decode_nn(p[0], args)
        print "LAYERS: " + str(no_layers) + " NEURONS: " + str(layers) + " FUNCTIONS: " + str(functions) + " FITNESS: " + str(p[1])

def write_to_file(nn, args):
    no_layers, layers, functions = decode_nn(nn, args)
    with open("config", "w") as f:
        f.write(str(no_layers) + "\n")
        for l in layers:
            f.write(str(l) + " ")
        f.write("\n")
        for fun in functions:
            f.write(str(fun) + " ")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pop_size", type = int, default = 20,
                        help="Population size")
    parser.add_argument("--max_layers", type = int, default = 1,
                        help="Max number of layers")
    parser.add_argument("--max_neuron_bits", type = int, default = 7,
                        help="Max number of bits for representing layer number")
    args = parser.parse_args()

    data = load_mnist()

    nn = genetic(args, data)

    write_to_file(nn, args)
