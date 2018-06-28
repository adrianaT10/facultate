import numpy
from random import randint

class HopfieldNetwork:
    CHAR_TO_INT = { "_": -1, "X": 1 }
    INT_TO_CHAR = { -1: "_", 1: "X" }

    # Initalize a Hopfield Network with N neurons
    def __init__(self, neurons_no):
        self.neurons_no = neurons_no
        self.state = numpy.ones((self.neurons_no), dtype=int)
        self.weights = numpy.zeros((self.neurons_no, self.neurons_no))
        self.crt_energy = 99999

# ------------------------------------------------------------------------------

    # Learn some patterns
    def learn_patterns(self, patterns, learning_rate):
        # TASK 1
        print len(patterns)
        sums = 0
        for pattern in patterns:
            pattern = [HopfieldNetwork.CHAR_TO_INT[x] for x in list(pattern)]
            sums += numpy.transpose([pattern]) * numpy.array([pattern])
        self.weights = numpy.subtract(sums, len(patterns))


    # Compute the energy of the current configuration
    def energy(self):
        # TASK 1:
        sums = 0.0
        for i in range(self.neurons_no):
            for j in range(self.neurons_no):
                sums += self.weights[i][j] * self.state[i] * self.state[j]
        return -1/2.0 * sums

    # Update a single random neuron
    def single_update(self):
        # TASK 1
        i = randint(0, self.neurons_no - 1)
        sums = 0
        for j in range(self.neurons_no):
            sums += self.weights[i][j] * self.state[j]
        self.state[i] = -1 if sums < 0 else 1


    # Check if energy is minimal
    def is_energy_minimal(self):
        # TASK 1
        e = self.energy()
        if e != self.crt_energy:
            self.crt_energy = e
            return False
        else:
            return True


    # --------------------------------------------------------------------------

    # Approximate the distribution of final states
    # starting from @samples_no random states.
    def get_final_states_distribution(self, samples_no=1000):
        # TASK 3
        return {}

    # -------------------------------------------------------------------------


    # Unlearn some patterns
    def unlearn_patterns(self, patterns, learning_rate):
        # TASK BONUS
        pass

    # -------------------------------------------------------------------------


    # Get the pattern of the state as string
    def get_pattern(self):
        return "".join([HopfieldNetwork.INT_TO_CHAR[n] for n in self.state])

    # Reset the state of the Hopfield Network to a given pattern
    def reset(self, pattern):
        assert(len(pattern) == self.neurons_no)
        for i in range(self.neurons_no):
            self.state[i] = HopfieldNetwork.CHAR_TO_INT[pattern[i]]

    # Reset the state of the Hopfield Network to a random pattern
    def random_reset(self):
        for i in range(self.neurons_no):
            self.state[i] = 1 - 2* numpy.random.randint(0, 2)

    def to_string(self):
        return HopfieldNetwork.state_to_string(self.state)

    @staticmethod
    def state_to_string(state):
        return "".join([HopfieldNetwork.INT_TO_CHAR[c] for c in state])

    @staticmethod
    def state_from_string(str_state):
        return numpy.array([HopfieldNetwork.CHAR_TO_INT[c] for c in str_state])

    # display the current state of the HopfieldNetwork
    def display_as_matrix(self, rows_no, cols_no):
        assert(rows_no * cols_no == self.neurons_no)
        HopfieldNetwork.display_state_as_matrix(self.state, rows_no, cols_no)

    @staticmethod
    def display_state_as_matrix(state, rows_no, cols_no):
        assert(state.size == rows_no * cols_no)
        print("")
        for i in range(rows_no):
            print("".join([HopfieldNetwork.INT_TO_CHAR[state[i*cols_no+j]]
                           for j in range(cols_no)]))
        print("")
