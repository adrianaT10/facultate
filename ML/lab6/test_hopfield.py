from hopfield import HopfieldNetwork
from argparse import ArgumentParser
from time import sleep
from os import path
from random import random, choice

# Reads all / first n patterns from specified file
# It returns the number of rows, the number of cols and the patterns

def read_patterns(args):
    assert(path.exists(args.patterns_path))
    with open(args.patterns_path) as in_file:
        patterns_no, rows_no, cols_no = \
                map(int, in_file.readline().strip().split())
        if args.patterns_no > 0:
            patterns_no = min(patterns_no, args.patterns_no)
        patterns = []
        for i in range(patterns_no):
            in_file.readline()                             # Skip the empty line
            patterns.append(
                "".join([in_file.readline().strip() for j in range(rows_no)])
            )
    return rows_no, cols_no, patterns

# ------------------------------------------------------------------------------

def train_hopfield(rows_no, cols_no, patterns, args):
    hopfield_net = HopfieldNetwork(rows_no * cols_no)
    hopfield_net.learn_patterns(patterns, args.train_lr)
    return hopfield_net

def apply_noise(pattern, noise):
    # TASK 1
    noise_pattern = ""
    for c in pattern:
        r = random()
        if r < noise:
            noise_pattern += "_" if c == "X" else "X"
        else:
            noise_pattern += c
    return noise_pattern

def show_one(hopfield_net, rows_no, cols_no, patterns, args):
    # Choose a pattern
    original_pattern = choice(patterns)
    hopfield_net.reset(original_pattern)
    hopfield_net.display_as_matrix(rows_no, cols_no)

    # Apply noise to it
    noisy_pattern = apply_noise(original_pattern, args.noise)      # apply noise
    hopfield_net.reset(noisy_pattern)    # The net starts from the noisy pattern
    hopfield_net.display_as_matrix(rows_no, cols_no)

    # Let the network reach an energetic mimimum
    while not hopfield_net.is_energy_minimal():
        hopfield_net.single_update()
        hopfield_net.display_as_matrix(rows_no, cols_no)
        print("Energy: %f" % hopfield_net.energy())

    print("Done!")

# ------------------------------------------------------------------------------

def test_hopfield(hopfield_net, patterns, args):
    # TASK 2: Testarea retelei
    # args.test_no - numarul de sabloane ce vor fi testate
    # intoarce acuratetea



    return 0.0

# ------------------------------------------------------------------------------

def show_histogram(hopfield_net, rows_no, cols_no, args):
    final_states = hopfield_net.get_final_states_distribution(args.samples_no)
    for k, v in final_states.items():
        for row in range(rows_no):
            print(k[row * cols_no : (row + 1) * cols_no])
        print("Probability: %f" % v)

# ------------------------------------------------------------------------------

def inverse(pattern):
    return ["_" if c == "X" else "X"  for c in pattern]

def unlearn(hopfield_net, patterns, args):
    # TASK BONUS: Uitarea sabloanelor nedorite
    # args.unlearn_no - numarul de sabloane testate
    # args.unlearn_rl - rata de invatare folosita la "dezvatare" :)

    pass

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--task", type = int, default = 1,
                        help="Task type.")
    parser.add_argument("--patterns_path", type = str, default = "digits",
                        help="File to read patterns from.")
    parser.add_argument("--patterns_no", type = int, default = 0,
                        help="Number of patterns to read from the file.")
    parser.add_argument("--noise", type = float, default = 0.15,
                        help="Noise level to apply to patterns.")
    parser.add_argument("--samples_no", type = int, default = 5000,
                        help="Number of samples to estimate final state dist.")
    parser.add_argument("--test_no", type = int, default = 100,
                        help="Number of patterns to use in test phase.")
    parser.add_argument("--unlearn_no", type = int, default = 100,
                        help="Number of patterns to use in test phase for unlearning.")
    parser.add_argument("--train_lr", type = float, default = 1.0,
                        help="Learning rate for the 'learn' phase.")
    parser.add_argument("--unlearn_lr", type = float, default = 0.01,
                        help="Learning rate for the 'unlearn' phase.")
    args = parser.parse_args()

    assert(args.task in [1,2,3,4])

    # Read the patterns
    rows_no, cols_no, patterns = read_patterns(args)

    # Train the hopfield network
    hopfield_net = train_hopfield(rows_no, cols_no, patterns, args)

    if args.task == 1:
        # Show one recovery
        show_one(hopfield_net, rows_no, cols_no, patterns, args)
    elif args.task == 2:
        # Print the accuracy of the hopfield net
        print("Accuracy: %f" % test_hopfield(hopfield_net, patterns, args))
    elif args.task == 3:
        # Show the histogram of final states
        show_histogram(hopfield_net, rows_no, cols_no, args)
    else:
        # Print the accuracy of the hopfield net
        print("Accuracy: %f" % test_hopfield(hopfield_net, patterns, args))

        # Do unlearning
        unlearn(hopfield_net, patterns, args)

        # Retest accuracy
        print("Accuracy: %f" % test_hopfield(hopfield_net, patterns, args))
