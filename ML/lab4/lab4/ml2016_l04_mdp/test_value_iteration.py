from value_iteration import Labyrinth, value_iteration

next_states_test_cases = {
    (2, 1, "UP") : {(1, 1): 0.8, (2, 1): 0.2},
    (3, 4, "RIGHT") : {},
    (4, 5, "RIGHT") : {(4, 5): 0.9, (3, 5): 0.1},
    (4, 2, "UP") : {(4,1): 0.1, (3,2): 0.8, (4,3): 0.1}
}

def test_next_states():
    l = Labyrinth("map1")
    for ((r,c,action), correct) in next_states_test_cases.items():
        next_states = l.get_next_states((r,c), action)
        assert(len(next_states) == len(correct))
        for s, p in correct.items():
            assert(s in next_states and abs(next_states[s] - p) < 0.00001)
    print("get_next_states seems to be ok!")

correct_utilities = {
    (1,1): 3.758331240949238, (1,2): 4.353040287870424,
    (1,3): 4.971520241313916, (1,4): 5.675898852752452,
    (1,5): 6.478107325394425, (2,1): 3.287779261512760,
    (2,5): 7.492009513009637, (3,1): 3.569124997321274,
    (3,2): 3.284429339915437, (3,3): -10.0, (3, 4): 10.0,
    (3,5): 8.546455296520545, (4,1): 4.114357734930523,
    (4,2): 4.767863283065356, (4,3): 5.629396108078685,
    (4,4): 8.378820091193806, (4,5): 7.579716056280081
}

correct_policy = {
    (1,1): 'RIGHT', (1,2): 'RIGHT', (1,3): 'RIGHT', (1,4): 'RIGHT',
    (1,5): 'DOWN',
    (2,1): 'UP', (2, 5): 'DOWN',
    (3,1): 'DOWN', (3, 2): 'LEFT', (3, 5): 'LEFT',
    (4,1): 'RIGHT', (4, 2): 'RIGHT', (4, 3): 'RIGHT', (4,4): 'UP', (4, 5): 'UP'
}

def test_value_iteration():
    l = Labyrinth("map1")
    utilities, policy = value_iteration(l, 0.9)

    assert(len(utilities) == len(correct_utilities))
    for s, u in correct_utilities.items():
        assert(s in utilities and abs(utilities[s] - u) < 0.01)
    print("utilities are ok!")

    for s, a in correct_policy.items():
        assert(s in policy and policy[s] == a)

    print("policy seems to be ok")

if __name__ == "__main__":
    test_next_states()
    test_value_iteration()
