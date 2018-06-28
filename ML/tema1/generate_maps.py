from random import random, choice, randint
from argparse import ArgumentParser
import os
import shutil
from copy import deepcopy

## Return room with walls, inaccesible spots (20%), treasures and guardian
def initialize_room(dim, prob_guard):
    m = [[' ' for i in range(dim)] for j in range(dim)]
    m[0] = ['*' for i in range(dim)]
    m[dim - 1] = ['*' for i in range(dim)]
    for i in range(1, dim - 1):
        m[i][0] = '*'
        m[i][dim - 1] = '*'

    # place inaccessible points
    for k in range((20 * dim * dim) / 100):
        i = randint(0, dim - 1)
        j = randint(0, dim - 1)
        m[i][j] = '*'

    # place treasures
    for k in range(3):
        (i, j) = pick_reacheable_spot(m)
        m[i][j] = '$'

    k = random()
    if k <= prob_guard:
        # place guardian
        (i, j) = pick_reacheable_spot(m)
        m[i][j] = 'B'
    return m

## Check if a position is surrounded by walls
def is_reachable(m, x, y):
    dim = len(m)
    if x > 0 and m[x - 1][y] != '*':
        return True
    if x < dim - 1 and m[x + 1][y] != '*':
        return True
    if y > 0 and m[x][y - 1] != '*':
        return True
    if y < dim - 1 and m[x][y + 1] != '*':
        return True
    return False 

def __serialize_state(state):
    return "\n".join(map(lambda row: "".join(row), state))

## Choose a random position on the map that is not between walls
def pick_reacheable_spot(room):
    dim = len(room)
    i = randint(1, dim - 2)
    j = randint(1, dim - 2)
    while room[i][j] != ' ' and not is_reachable(room, i, j):
        i = randint(1, dim - 2)
        j = randint(1, dim - 2)

    return (i, j)

## Randomly place portals from one room to another
def place_portals(rooms, args):
    if args.no_rooms == 1:
        return rooms, []
    available = range(0, args.no_rooms)
    # ((room1, r1, c1), (room2, r2, c2))
    portals = []

    r = choice(available)
    available.remove(r)
    r_portal = pick_reacheable_spot(rooms[r])
    rooms[r][r_portal[0]][r_portal[1]] = 'P'

    for i in range(args.no_rooms - 1):
        next = choice(available)
        available.remove(next)

        next_portal = pick_reacheable_spot(rooms[next])
        portals.append(((r, r_portal[0], r_portal[1]), (next, next_portal[0], next_portal[1])))
        rooms[next][next_portal[0]][next_portal[1]] = 'P'

        r = next
        r_portal = pick_reacheable_spot(rooms[r])
        rooms[r][r_portal[0]][r_portal[1]] = 'P'

    rooms[r][r_portal[0]][r_portal[1]] = ' '

    return rooms, portals

def is_valid_cell(room, row, col):
    return row >= 0 and row < len(room) and \
        col >= 0 and col < len(room) and \
        room[row][col] != "*"

## Check if there is a path from the start position to the exit
def verify_path(rooms, portals, crt_room, row, col, prev_room):
    ACTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    if rooms[crt_room][row][col] == 'O':
        return True

    rooms[crt_room][row][col] = '*'

    # check with DFS
    for action in ACTIONS:
        next_row = row + action[0]
        next_col = col + action[1]

        if not is_valid_cell(rooms[crt_room], next_row, next_col):
            continue
        # check for portals to a new room
        if rooms[crt_room][next_row][next_col] == 'P':
            for portal in portals:
                if portal[0] == (crt_room, next_row, next_col) and \
                    portal[1][1] != prev_room:
                    res =  verify_path(rooms, portals, portal[1][0], \
                        portal[1][1], portal[1][2], crt_room)
                    if res == True:
                        return True
        else:
            res = verify_path(rooms, portals, crt_room, next_row, next_col, prev_room)
            if res == True:
                return True
    return False

## Generate the map
def generate(args):
    rooms = []
    for i_room in range(args.no_rooms):
        room = initialize_room(args.dim, args.prob_guardians)
        rooms.append(room)

    # put portals on the map
    rooms, portals = place_portals(rooms, args)

    # place exit
    out_room = randint(0, args.no_rooms - 1)
    pos = pick_reacheable_spot(rooms[out_room])
    rooms[out_room][pos[0]][pos[1]] = 'O'

    # place Gigel
    start_room = randint(0, args.no_rooms - 1)
    start_pos = pick_reacheable_spot(rooms[start_room])
    
    return rooms, portals, start_room, start_pos
    
## Write map to files
def write_config(rooms, portals, start_room, start_pos, args):
    print 'Start pos ' + str(start_pos) + " " + str(start_room)

    shutil.rmtree(args.folder, ignore_errors=True)
    os.mkdir(args.folder)

    for i_room in range(args.no_rooms):
        filename = args.folder + '/room_' + str(i_room)
        with open(filename, 'w') as f:
            state = __serialize_state(rooms[i_room])
            f.write(state)
            print 'Room ' + str(i_room)
            print(state)
        f.close()

    # write start position + portals
    filename = args.folder + '/config'
    print 'Portals'
    with open(filename, 'w') as f:
        f.write(str(start_room) + " " + str(start_pos[0]) + " " + str(start_pos[1]))
        f.write('\n')
        for pair in portals:
            f.write(str(pair))
            f.write('\n')
            print str(pair)
    f.close()



if __name__ == "__main__":
    parser = ArgumentParser()
    # Input file
    parser.add_argument("--folder", type = str, default = "default",
                        help = "Folder to put the files.")
    # No of rooms to generate
    parser.add_argument("--no_rooms", type = int, default = 1,
                        help = "Number of rooms")
    # Room size (one side)
    parser.add_argument("--dim", type = int, default = 8,
                        help = "Room dimension")
    # Probabily of a guardian in a room
    parser.add_argument("--prob_guardians", type = int, default = 0.5,
                        help = "Number of guardians")

    args = parser.parse_args()

    rooms, portals, start_room, start_pos = generate(args)

    while not verify_path(deepcopy(rooms), portals, start_room, start_pos[0], start_pos[1], start_room):
        rooms, portals, start_room, start_pos = generate(args)

    write_config(rooms, portals, start_room, start_pos, args)
    