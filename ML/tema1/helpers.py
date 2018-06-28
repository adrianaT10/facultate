from copy import copy
from random import choice
from math import sqrt
from glob import glob
from state import State

ACTIONS = ["UP", "RIGHT", "DOWN", "LEFT", "STAY"]
ACTION_EFFECTS = {
    "UP": (-1,0),
    "RIGHT": (0,1),
    "DOWN": (1,0),
    "LEFT": (0,-1),
    "STAY": (0,0)
}

MOVE_REWARD = -0.1
TREASURE_REWARD = 0.2
WIN_REWARD = 1.0
LOSE_REWARD = -20.0
MIN_SCORE = -20.0

GUARD_RADIUS = 3.0


## Functions to serialize / deserialize game states
def __serialize_state(state):
    return "\n".join(map(lambda row: "".join(row), state))

def __deserialize_state(str_state):
    return list(map(list, str_state.split("\n")))

## Return the initial state of the game
def get_initial_state(map_file_path):
    with open(map_file_path) as map_file:
        initial_str_state = map_file.read().strip()
    return initial_str_state

## Return the available actions in a given state
def get_legal_actions(state):
    actions = []
    for a in ACTIONS:
        next_x = state.get_x_position() + ACTION_EFFECTS[a][0]
        next_y = state.get_y_position() + ACTION_EFFECTS[a][1]
        if __is_valid_cell(State.ROOMS[state.get_room()], next_x, next_y):
            actions.append(a)

    return actions

def get_all_actions():
    return copy(ACTIONS)

## Get the coordinates of an actor
def __get_position(state, marker):
    for row_idx, row in enumerate(state):
        if marker in row:
            return row_idx, row.index(marker)
    return -1, -1

## Check if is a final state
def is_final_state(state, score):
    return score < MIN_SCORE or state.is_final_state()

## Check if the given coordinates are valid (on map and not a wall)
def __is_valid_cell(state, row, col):
    return row >= 0 and row < len(state) and \
        col >= 0 and col < len(state[row]) and \
        state[row][col] != "*"

## Check if given position is valid for a guardian
## (is on map, not on a wall or portal)
def __is_valid_cell_guardian(state, row, col):
    return row >= 0 and row < len(state) and \
        col >= 0 and col < len(state[row]) and \
        state[row][col] != "*" and \
        state[row][col] != "P" and \
        state[row][col] != "O"

## Return the reward for pssing through a portal
def __get_portal_reward(state):
    field = __deserialize_state(state.get_visible_field())
    # if he sees the exit but tries to go through a portal, give negative reward
    if __get_position(field, "O")[0] != -1:
        return -5
    return MOVE_REWARD

def get_reward(state):
    field = __deserialize_state(state.get_visible_field())
    guard_pos = __get_position(field, "B")
    treasure_pos = __get_position(field, "$")
    exit_pos = __get_position(field, "O")

    if exit_pos != (-1, -1):
        if guard_pos == (-1, -1):
            print 'lala3'
            return -0.05
        else:
            print 'lala4'
            return -0.1
    return MOVE_REWARD

## Move to next state
def apply_action(state, action, used_portal):
    assert(action in ACTIONS)
    message = "Gigel moved %s." % action

    room = State.ROOMS[state.get_room()]
    g_row, g_col = state.x, state.y
    assert(g_row >= 0 and g_col >= 0)             # Gigel must be on the map

    next_g_row = g_row + ACTION_EFFECTS[action][0]
    next_g_col = g_col + ACTION_EFFECTS[action][1]

    if not __is_valid_cell(room, next_g_row, next_g_col):
        next_g_row = g_row
        next_g_col = g_col
        message = message + " Not a valid cell there."

    # Redraw the portal on the map after Gigel stepped on it
    if used_portal:
        room[g_row][g_col] = "P"
        used_portal = False
    else:
        room[g_row][g_col] = " "

    if room[next_g_row][next_g_col] == "B":
        message = message + " Gigel stepped on the balaur."
        state.is_final_state(True)
        return LOSE_REWARD, message, used_portal

    elif room[next_g_row][next_g_col] == '$':
        message = message + " Gigel got a treasure."
        state.update_position(next_g_row, next_g_col)
        return TREASURE_REWARD, message, used_portal

    elif room[next_g_row][next_g_col] == 'P':
        message = message + " Gigel went through the portal"
        # find the other end of the portal
        for (r1, c1, next_room, r2, c2) in State.PORTALS[state.get_room()]:
            if r1 == next_g_row and c1 == next_g_col:
                reward = __get_portal_reward(state)
                message += " to room " + str(next_room) + " position " + \
                            str((r2, c2))
                state.change_room(next_room)
                state.update_position(r2, c2)
                return reward, message, True

    elif room[next_g_row][next_g_col] == "O":
        state.update_position(next_g_row, next_g_col)
        state.is_final_state(True)
        message = message + " Gigel GOT OUT!"
        return WIN_REWARD, message, used_portal

    state.update_position(next_g_row, next_g_col)
    reward = MOVE_REWARD

    ## Guardian moves now
    b_row, b_col = __get_position(room, "B")
 
    if b_row == -1:
        return reward, message, used_portal

    dy, dx = next_g_row - b_row, next_g_col - b_col

    # move towards Gigel only if he is within guardian's radius
    if sqrt(dy*dy + dx * dx) > GUARD_RADIUS:
        return reward, message, used_portal

    is_good = lambda dr, dc:__is_valid_cell_guardian(room, b_row + dr, b_col + dc)

    next_b_row, next_b_col = b_row, b_col
    if abs(dy) > abs(dx) and is_good(int(dy / abs(dy)), 0):
        next_b_row = b_row + int(dy / abs(dy))
    elif abs(dx) > abs(dy) and is_good(0, int(dx / abs(dx))):
        next_b_col = b_col + int(dx / abs(dx))
    else:
        options = []
        if abs(dx) > 0:
            if is_good(0, int(dx / abs(dx))):
                options.append((b_row, b_col + int(dx / abs(dx))))
        else:
            if is_good(0, -1):
                options.append((b_row, b_col - 1))
            if is_good(0, 1):
                options.append((b_row, b_col + 1))
        if abs(dy) > 0:
            if is_good(int(dy / abs(dy)), 0):
                options.append((b_row + int(dy / abs(dy)), b_col))
        else:
            if is_good(-1, 0):
                options.append((b_row - 1, b_col))
            if is_good(1, 0):
                options.append((b_row + 1, b_col))

        if len(options) > 0:
            next_b_row, next_b_col = choice(options)

    if next_b_row == state.get_x_position() and next_b_col == state.get_y_position():
        message = message + " The balaur ate Gigel."
        state.is_final_state(True)
        reward = LOSE_REWARD
    else:
        message = message + " The balaur follows Gigel."
        reward = MOVE_REWARD

    room[b_row][b_col] = " "
    room[next_b_row][next_b_col] = "B"

    return reward, message, used_portal

## Read the map
def read_config(args):
    global MIN_SCORE
    
    portals = {}    # room1: (r1, c1, room2, r2, c2)
    with open(args.folder + '/config') as f:
        aux = f.readline().split(" ")
        start_room = int(aux[0])
        start_pos = (int(aux[1]), int(aux[2]))
        for line in f:
            aux = line.split(',')
            aux = [int(a.strip('()\n ')) for a in aux]
            if aux[0] not in portals:
                portals[aux[0]] = [(aux[1], aux[2], aux[3], aux[4], aux[5])]
            else:
                portals[aux[0]].append((aux[1], aux[2], aux[3], aux[4], aux[5]))
            if aux[3] not in portals:
                portals[aux[3]] = [(aux[4], aux[5], aux[0], aux[1], aux[2])]
            else:
                portals[aux[3]].append((aux[4], aux[5], aux[0], aux[1], aux[2]))

    rooms = []
    no_rooms = len(portals) if len(portals) > 0 else 1
    for i in range(no_rooms):
        path = args.folder + '/room_' + str(i)
        rooms.append(__deserialize_state(get_initial_state(path)))

    # number of moves is given by the map area
    MIN_SCORE = -no_rooms * len(rooms[0]) * len(rooms[0]) / 10.0

    return start_room, start_pos, rooms, portals

def display_state(state):
    room = put_Gigel_on_map(state)

    print(room)
    

def put_Gigel_on_map(state):
    room = copy(State.ROOMS[state.get_room()])
    if state.get_x_position() != -1:
        room[state.get_x_position()][state.get_y_position()] = "G"
    return __serialize_state(room)
