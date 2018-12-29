from sys import argv
from copy import copy, deepcopy
from math import sqrt

class Labyrinth:

    ACTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]

    def __init__(self, filename):

        # Read labyrinth description from file
        with open(filename) as f:

            # Read probabilities
            self.p = list(map(float, f.readline().split()))

            # Read map size
            self.height, self.width = map(int, f.readline().split())

            # Read the number of final states and each of them
            final_states_no = int(f.readline().strip())
            self.final_states = {}
            for i in range(final_states_no):
                line = f.readline().strip().split()
                self.final_states[(int(line[0]), int(line[1]))] = float(line[2])

            # Read the reward for a non-terminal state
            self.default_reward = float(f.readline().strip())

            # Read the map (' ' for empty cells, '*' for walls)
            self.states = set()
            for row in range(self.height):
                line = f.readline().strip()
                for col in range(self.width):
                    if line[col] == ' ':
                        self.states.add((row, col))

    def get_all_states(self):
        return copy(self.states)

    def get_valid_actions(self, state):
        return copy(self.ACTIONS) if not self.is_final_state(state) else []

    def is_valid_state(self, state):
        return state in self.states

    def is_final_state(self, state):
        return state in self.final_states

    def get_reward(self, state):
        return self.final_states.get(state, self.default_reward)

    def get_next_states(self, state, action):

        # TODO (1)
        if self.is_final_state(state):
            return {}
        res = {}
        res[state] = 0
        (y, x) = state
        next_states = {'UP': (y - 1, x), 'DOWN': (y + 1, x), 'LEFT': (y, x - 1), 'RIGHT': (y, x + 1)}
        if action == 'UP':
            actions = ['UP', 'LEFT', 'RIGHT']
        elif action == 'LEFT':
            actions = ['LEFT', 'UP', 'DOWN']
        elif action == 'RIGHT':
            actions = ['RIGHT', 'UP', 'DOWN']
        elif action == 'DOWN':
            actions = ['DOWN', 'LEFT', 'RIGHT']

        for a in actions:
            poz = next_states[a]
            if self.is_valid_state(poz):
                if a == action:
                    res[poz] = 0.8
                else:
                    res[poz] = 0.1
            else:
                if a == action:
                    res[state] += 0.8
                else:
                    res[state] += 0.1

        if res[state] == 0:
            del res[state]

        return res

    def print_utilities(self, U, precision = 3):
        fmt = "%%%d.%df" % (precision + 4, precision)
        wall = "*" * (precision + 4)
        print("Utilities:")
        for r in range(self.height):
            print(" ".join([(fmt % U[(r,c)]) if (r,c) in self.states else wall
                    for c in range(self.width)]))
        print("")

    def print_policy(self, policy):
        fmt = " %%%ds " % max(map(len, self.ACTIONS))
        wall = "*" * max(map(len, self.ACTIONS))
        print("Policy:")
        for r in range(self.height):
            line = [fmt % policy.get((r,c), wall) for c in range(self.width)]
            print(" ".join(line))
        print("")

    def print_rewards(self, precision = 2):
        fmt = "%%%d.%df" % (precision + 4, precision)
        wall = "*" * (precision + 4)
        print("Rewards:")
        for r in range(self.height):
            line = []
            for c in range(self.width):
                if (r,c) in self.states:
                    line.append(
                        fmt % self.final_states.get((r,c), self.default_reward)
                    )
                else:
                    line.append(wall)
            print(" ".join(line))
        print("")

def value_iteration(game, discount = 0.9, max_diff = 0.0001):

    # TODO (2)

    U = {state: 0 for state in game.get_all_states()}
    Uprim = {state: game.get_reward(state) for state in game.get_all_states()}
    policy = {state: "UP" for state in game.get_all_states()}

    print(game.get_next_states((4, 5), 'RIGHT'))
    first = True

    while udiff(U, Uprim) > max_diff or first == True:
        U = deepcopy(Uprim)
        for state in game.get_all_states():
            maxval = -999
            for a in game.get_valid_actions(state):
                val = 0
                T = game.get_next_states(state, a)
                for (s,t) in T.items():
                    val += t * U[s]
                if val > maxval:
                    maxval = val
                    best_act = a
            if maxval  == -999:
                continue
            Uprim[state] = game.get_reward(state) + discount * maxval
            policy[state] = best_act
            first = False

    return U, policy

def udiff(U, V):
    sum = 0
    for (s, u) in U.items():
        sum += (u - V[s]) * (u - V[s]) 
    return sqrt(sum) / len(U)


if __name__ == "__main__":
    l = Labyrinth(argv[1])
    l.print_rewards()
    u, policy = value_iteration(l)
    l.print_utilities(u)
    l.print_policy(policy)
