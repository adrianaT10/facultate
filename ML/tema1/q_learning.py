# General imports
from copy import copy
from random import choice, random
from argparse import ArgumentParser
from time import sleep

# Game functions
from helpers import ( get_initial_state,       # get initial state from file
                          get_legal_actions,  # get the legal actions in a state
                          get_all_actions,
                          is_final_state,         # check if a state is terminal
                          apply_action,       # apply an action in a given state
                          display_state,            # display the current state
                          read_config )
from state import State

VISION_RADIUS = 8


def epsilon_greedy(Q, state, legal_actions, epsilon):
    # go to unexplored states first
    unexplored = []
    save_state = state.save_state()
    for a in legal_actions:
        if (save_state, a) not in Q:
            unexplored.append(a)
    if len(unexplored) > 0:
        return choice(unexplored)

    # choose a random action with a probability
    r = random()
    if r <= epsilon:
        return choice(legal_actions)

    # return best action
    max_val = -999
    for a in legal_actions:
        if Q[(save_state, a)] > max_val:
            max_val = Q[(save_state, a)]
            best_action = a

    return best_action

def best_action(Q, state, legal_actions):
    max_val = -999
    save_state = state.save_state()
    best_a = choice(legal_actions)
    for a in legal_actions:
        if (save_state, a) in Q and Q[(save_state, a)] > max_val:
            max_val = Q[(save_state, a)]
            best_a = a

    return best_a

## Return next action best on chosen strategy
def choose_action(Q, state, legal_actions, args):
    if args.type == 'random':
        return choice(legal_actions)
    if args.type == 'epsilon':
        return epsilon_greedy(Q, state, legal_actions, args.epsilon)
    if args.type == 'best':
        return epsilon_greedy(Q, state, legal_actions, 0)

def q_learning(args):
    Q = {}
    train_scores = []
    eval_scores = []
    no_wins = 0
    train_ep = 0
    wins = []
                                                          # for each episode ...
    # for train_ep in range(1, args.train_episodes + 1):
    while train_ep <= args.train_episodes :

                                                    # ... get the initial state,
        score = 0
        start_room, start_pos, State.ROOMS, State.PORTALS = read_config(args)
        state = State(start_room, args.vision_radius)
        state.update_position(start_pos[0], start_pos[1])

        used_portal = False

                                               # display current state and sleep
        if args.verbose:
            display_state(state); sleep(args.sleep)

                                           # while current state is not terminal
        while not is_final_state(state, score):

                                               # choose one of the legal actions
            actions = get_legal_actions(state)
            action = choose_action(Q, state, actions, args)
            save_state_old = state.save_state()

                            # apply action and get the next state and the reward
            reward, msg, used_portal = apply_action(state, action, used_portal)
            score += reward

            # Q-Learning
            save_state = state.save_state()
            max_val = -9999
            for a_new in get_all_actions():
                if (save_state, a_new) in Q and Q[(save_state, a_new)] > max_val:
                    max_val = Q[(save_state, a_new)]

            if max_val == -9999:
                max_val = 0

            if (save_state_old, action) in Q:
                Q[(save_state_old, action)] += args.learning_rate * (reward + \
                            args.discount * max_val - Q[save_state_old, action])
            else:
                Q[(save_state_old, action)] = args.learning_rate * (reward + \
                                            args.discount * max_val)

                                               # display current state and sleep
            if args.verbose:
                print(msg); display_state(state); sleep(args.sleep)

            if "Gigel GOT OUT!" in msg:
                no_wins += 1

        # print("Episode %6d / %6d" % (train_ep, args.train_episodes))
        train_scores.append(score)  
        wins.append(no_wins)      

                                                    # evaluate the greedy policy
        if train_ep % args.eval_every == 0:
            avg_score = .0

            for s in train_scores[-args.eval_every:]:
                avg_score += s

            eval_scores.append(avg_score / args.eval_every)

        train_ep += 1

    print "Gigel had " + str(no_wins) + " wins"

    # --------------------------------------------------------------------------
    if args.final_show:
        final_score = 0
        start_room, start_pos, State.ROOMS, State.PORTALS = read_config(args)
        state = State(start_room, args.vision_radius)
        state.update_position(start_pos[0], start_pos[1])

        used_portal = False

        while not is_final_state(state, final_score):
            action = best_action(Q, state, get_legal_actions(state))
            reward, msg, used_portal = apply_action(state, action, used_portal)
            final_score += reward
            print(msg); display_state(state); sleep(args.sleep)

    if args.plot_scores:
        from matplotlib import pyplot as plt
        import numpy as np
        plt.xlabel("Episode")
        plt.ylabel("Average Score")
        # plt.plot(
        #     np.linspace(1, args.train_episodes, args.train_episodes),
        #     np.convolve(train_scores, [0.2,0.2,0.2,0.2,0.2], "same"),
        #     linewidth = 1.0, color = "blue"
        # )
        plt.plot(
            np.linspace(args.eval_every, train_ep, len(eval_scores)),
            eval_scores, linewidth = 2.0, color = "red"
        )
        plt.show()

    return train_scores, wins

if __name__ == "__main__":
    parser = ArgumentParser()
    # Folder for input files
    parser.add_argument("--folder", type = str, default = "default",
                        help = "Folder to read map from.")
    # Gigel's vision radius
    parser.add_argument("--radius", dest="vision_radius", type = int, default = 8,
                        help = "Vision radius.")
    # Strategy for choosing next action
    parser.add_argument("--type", type = str, default = "best",
                        help = "random | epsilon | best")
    parser.add_argument("--learning_rate", type = float, default = 0.1,
                        help = "Learning rate")
    parser.add_argument("--discount", type = float, default = 0.99,
                        help = "Value for the discount factor")
    parser.add_argument("--epsilon", type = float, default = 0.15,
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
