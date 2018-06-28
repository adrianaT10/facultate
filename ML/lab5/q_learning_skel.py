# Tudor Berariu, 2016

# General imports
from copy import copy
from random import choice, random
from argparse import ArgumentParser
from time import sleep

# Game functions
from mini_pacman import ( get_initial_state,       # get initial state from file
                          get_legal_actions,  # get the legal actions in a state
                          is_final_state,         # check if a state is terminal
                          apply_action,       # apply an action in a given state
                          display_state )            # display the current state

def epsilon_greedy(Q, state, legal_actions, epsilon):
    # TODO (2) : Epsilon greedy
    unexplored = []
    for a in legal_actions:
        if (state, a) not in Q:
            unexplored.append(a)
    if len(unexplored) > 0:
        return choice(unexplored)

    r = random()
    if r <= epsilon:
        return choice(legal_actions)

    max_val = -999
    for a in legal_actions:
        if Q[(state, a)] > max_val:
            max_val = Q[(state, a)]
            best_action = a

    return best_action

def best_action(Q, state, legal_actions):
    # TODO (3) : Best action
    max_val = -999
    for a in legal_actions:
        if (state, a) in Q and Q[(state, a)] > max_val:
            max_val = Q[(state, a)]
            best_action = a

    return best_action

def q_learning(args):
    Q = {}
    train_scores = []
    eval_scores = []
                                                          # for each episode ...
    for train_ep in range(1, args.train_episodes + 1):

                                                    # ... get the initial state,
        score = 0
        state = get_initial_state(args.map_file)

                                               # display current state and sleep
        if args.verbose:
            display_state(state); sleep(args.sleep)

                                           # while current state is not terminal
        while not is_final_state(state, score):

                                               # choose one of the legal actions
            actions = get_legal_actions(state)
            action = epsilon_greedy(Q, state, actions, args.epsilon)

                            # apply action and get the next state and the reward
            state_new, reward, msg = apply_action(state, action)
            score += reward

            # TODO (1) : Q-Learning
            max_val = -9999
            for a_new in get_legal_actions(state_new):
                if (state_new, a_new) in Q and Q[(state_new, a_new)] > max_val:
                    max_val = Q[(state_new, a_new)]
                    best_action = a_new

            if max_val == -9999:
                max_val = 0

            if (state, action) in Q:
                Q[(state, action)] += args.learning_rate * (reward + args.discount * max_val - Q[state, action])
            else:
                Q[(state, action)] = args.learning_rate * (reward + args.discount * max_val)

            state = state_new

                                               # display current state and sleep
            if args.verbose:
                print(msg); display_state(state); sleep(args.sleep)

        print("Episode %6d / %6d" % (train_ep, args.train_episodes))
        train_scores.append(score)

                                                    # evaluate the greedy policy
        if train_ep % args.eval_every == 0:
            avg_score = .0

            # TODO (4) : Evaluate

            eval_scores.append(avg_score)

    # --------------------------------------------------------------------------
    if args.final_show:
        state = get_initial_state(args.map_file)
        final_score = 0
        while not is_final_state(state, final_score):
            action = best_action(Q, state, get_legal_actions(state))
            state, reward, msg = apply_action(state, action)
            final_score += reward
            print(msg); display_state(state); sleep(args.sleep)

    if args.plot_scores:
        from matplotlib import pyplot as plt
        import numpy as np
        plt.xlabel("Episode")
        plt.ylabel("Average score")
        plt.plot(
            np.linspace(1, args.train_episodes, args.train_episodes),
            np.convolve(train_scores, [0.2,0.2,0.2,0.2,0.2], "same"),
            linewidth = 1.0, color = "blue"
        )
        plt.plot(
            np.linspace(args.eval_every, args.train_episodes, len(eval_scores)),
            eval_scores, linewidth = 2.0, color = "red"
        )
        plt.show()

if __name__ == "__main__":
    parser = ArgumentParser()
    # Input file
    parser.add_argument("--map_file", type = str, default = "mini_map",
                        help = "File to read map from.")
    # Meta-parameters
    parser.add_argument("--learning_rate", type = float, default = 0.1,
                        help = "Learning rate")
    parser.add_argument("--discount", type = float, default = 0.99,
                        help = "Value for the discount factor")
    parser.add_argument("--epsilon", type = float, default = 0.05,
                        help = "Probability to choose a random action.")
    # Training and evaluation episodes
    parser.add_argument("--train_episodes", type = int, default = 1000,
                        help = "Number of episodes")
    parser.add_argument("--eval_every", type = int, default = 10,
                        help = "Evaluate policy every ... games.")
    parser.add_argument("--eval_episodes", type = float, default = 10,
                        help = "Number of games to play for evaluation.")
    # Display
    parser.add_argument("--verbose", dest="verbose",
                        action = "store_true", help = "Print each state")
    parser.add_argument("--plot", dest="plot_scores", action="store_true",
                        help = "Plot scores in the end")
    parser.add_argument("--sleep", type = float, default = 0.1,
                        help = "Seconds to 'sleep' between moves.")
    parser.add_argument("--final_show", dest = "final_show",
                        action = "store_true",
                        help = "Demonstrate final strategy.")
    args = parser.parse_args()
    q_learning(args)
