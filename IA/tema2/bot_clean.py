import sys
from copy import deepcopy
from random import randint
from Lab05 import make_atom, make_const, make_var, get_head, unify, substitute, print_formula, get_value, get_args, is_variable, is_constant, get_name

FILENAME = 'sample.in'
ROOM = 'room'
WAREHOUSE = 'warehouse'
CLEAN = 'Clean'
MOVE = 'Move'
REFILL = 'Refill'
HEIGHT = 3

graph = {}
Capacity = 0
Rooms = []
Actions = [MOVE, CLEAN, REFILL]
Time = 0
Reward = 0

class State:
	def __init__(self, location, ):
		self.location = location
		self.substances = {}
		self.dirty_rooms = []

	def carries(self, s, val):
		self.substances[s] = val

	def add_dirty_room(self, room):
		self.dirty_rooms.append(room)

	def is_in_dirty_room(self):
		return self.location in self.dirty_rooms

	def can_clean(self):
		if self.location not in self.dirty_rooms:
			return False
		room = Rooms[self.location]
		for (subst, q) in room.substances:
			if self.substances[subst] < q:
				return False
		return True

	def can_clean_room(self, index):
		if index not in self.dirty_rooms:
			return False
		room = Rooms[index]
		for (subst, q) in room.substances:
			if self.substances[subst] < q:
				return False
		return True

	def clean_cost(self):
		return Rooms[self.location].dimension

	def can_move(self):
		if self.location not in graph:
			return False
		return True

	def move_options(self):
		return graph[self.location]

	def can_refill(self):
		if not Rooms[self.location].is_warehouse():
			return False
		for (subst, q) in self.substances.items():
			if q < Capacity:
				return True

	def is_final_state(self):
		return not self.dirty_rooms

	def apply_clean(self):
		self.dirty_rooms.remove(self.location)
		for (s, q) in Rooms[self.location].substances:
			self.substances[s] = self.substances[s] - q

	def apply_move(self, dest):
		self.location = dest

	def apply_refill(self):
		for subst in self.substances.keys():
			self.substances[subst] = Capacity

	def __str__(self):
		return "I am at " + str(self.location)

class Room:
	def __init__(self, number, room_type=ROOM):
		self.number = number
		self.room_type = room_type
		self.substances = []
		self.dimension = 0

	def set_roomtype(self, room_type):
		self.room_type = room_type

	def set_dimension(self, dimension):
		self.dimension = dimension

	def add_substance(self, s, val):
		self.substances.append((s, val))

	def is_warehouse(self):
		return self.room_type == WAREHOUSE

	def is_room(self):
		return self.room_type == ROOM

	def __str__(self):
		return "Room no " + str(self.number) + ", " + self.room_type + ", dim " + str(self.dimension)

class Action:
	def __init__(self, name, args):
		self.name = name

	def move_action(r1, r2, cost):
		self.r1 = r1
		self.r2 = r2
		self.cost = cost
		self.reward = reward


def makeplan(filename):
	state = read_environment(filename)
	path = []
	path =  forward(state, path)
	print(path)
	return path

def forward(state, path):
	global Time, Reward
	if state.is_final_state() or Time <= 0:
		return path

	action = find_best_action(state, path)
	if action == None:
		return path

	if action[0] == 'MANY':
		action_plan = action[1]
		for action in action_plan:
			old_location = state.location
			print("applying action " + str(action))
			[Time, Reward] = apply_action(state, Time, Reward, action)
			print("TIME " + str(Time))
			action_string = construct_action(action, old_location, state.location)
			path.append(action_string)

			if state.can_refill():
				old_location = state.location
				action = (REFILL)
				[Time, Reward] = apply_action(state, Time, Reward, action)
				action_string = construct_action(action, old_location, state.location)
				path.append(action_string)
		# action = action[1][0]
	else:
		#print("Old State")
		#print(state)
		old_location = state.location
		print("applying action " + str(action))
		[Time, Reward] = apply_action(state, Time, Reward, action)
		print("TIME " + str(Time))
		action_string = construct_action(action, old_location, state.location)
		path.append(action_string)
		#print("New State")
		#print(state)

	#return path
	return forward(state, path)

def find_best_action(state, path):
	if state.can_clean():
		return (CLEAN)
	# if state.can_refill():
	# 	return (REFILL)
	
	options = state.move_options()
	if len(options) == 1 :
		return (MOVE, options[0][0], options[0][1])

	prevLoc = None
	if len(path) > 0 and get_action_name(path[-1]) == MOVE:
		args = get_action_args(path[-1])
		prevLoc = args[0]
	
	if state.can_move():
		actions_path = best_move_action(state, Time, prevLoc)
		if actions_path == None:
			return None
		else:
			return ('MANY', actions_path)

def best_move_action(state, time, prevLoc):
	cleanable_rooms = []
	must_refill = False

	for room in state.dirty_rooms:
		if state.can_clean_room(room):
			cleanable_rooms.append(room)
	if not cleanable_rooms:
		must_refill = True
	print("Cleanable rooms " + str(cleanable_rooms))

	initial_loc = state.location
	# (loc, timp, cost, parinte)
	queue = []
	# locatie: (cost, parinte)
	visited = {prevLoc: (-1, None)}
	# (loc, cost, parinte)
	best_refill  = (None, 9999, None)
	best_clean = (None, 9999, None)
	move_options = state.move_options()
	for (neigh, cost) in move_options:
		queue.append((neigh, time - cost, cost, state.location))
		visited[neigh] = (cost, state.location)

	reconstruct = False
	while queue:
		(loc, timp, cost, parent) = queue.pop(0)
		if timp <= 0:
			continue
		if Rooms[loc].is_warehouse() and timp >= 1:
			#reconstruct PATH
			if cost < best_refill[1]:
				reconstruct = True
				best_refill = (loc, cost, parent)
		if state.can_clean_room(loc):
			#reconstruct path
			if cost < best_clean[1] and timp - Rooms[loc].dimension >= 0:
				reconstruct = True
				best_clean = (loc, cost, parent)
				continue
		for (n, c) in graph[loc]:
			if n != parent:
				if n not in visited:
					visited[n] = (cost + c, loc)
					queue.append((n, timp - c, cost + c, loc))
				elif n in visited and cost + c < visited[n][0]:
					visited[n] = (cost + c, loc)
					queue.append((n, timp - c, cost + c, loc))

	if reconstruct:
		temp_state = deepcopy(state)
		temp_state.location = best_refill[0]
		if must_refill or (best_refill[1] < best_clean[1] and len(cleanable_rooms) < len(state.dirty_rooms) and \
			temp_state.can_refill()) or best_clean[0] == None:
			must_refill = True
			(loc, cost, parent) = best_refill
		else:
			(loc, cost, parent) = best_clean
		actions_path = []

		while parent != initial_loc:
			(c, p) = visited[parent]
			actions_path.insert(0, (MOVE, loc, cost - c))
			loc = parent
			parent = p
			cost = c
		
		actions_path.insert(0, (MOVE, loc, cost))
		if must_refill:
			actions_path.append((REFILL))
		else:
			actions_path.append((CLEAN))

		print("RECONSTRUCTED PATH " + str(actions_path))

		return actions_path
	
	print("No good move found");
	return None
			


def apply_action(state, time, reward, action):
	if action[0] == MOVE:
		state.apply_move(action[1])
		time = time - action[2]
	elif action == REFILL:
		state.apply_refill()
		time = time - 1
	elif action == CLEAN:
		state.apply_clean()
		time = time - state.clean_cost()
		print('Clean cost ' + str(state.clean_cost()))
		reward = reward + state.clean_cost()
	return [time, reward]

def first_clean(state, time, cost, parent):
	if time <= 0:
		return None
	temp_state = deepcopy(state)
	visited = [parent]
	queue = [(state.location, deepcopy(state.substances), time, cost)]

	while queue:
		(loc, subst, t, c) = queue.pop(0)
		visited.append(loc)
		temp_state.location = loc
		temp_state.substances = subst
		#print("current location " + str(loc) + " time " + str(t) + " cost " + str(c))
		#print("can clean " + str( temp_state.can_clean()))
		if temp_state.can_refill() and t > 1:
			temp_state.apply_refill()
			t = t - 1
			c = c + 1
		elif (temp_state.can_clean() and t - temp_state.clean_cost() >= 0):
			return c
		neighbours = graph[loc]
		for (neigh, cost) in neighbours:
			if t - cost > 0 and neigh not in visited:
				#print("add neighbour " + str(neigh))
				queue.append((neigh, deepcopy(temp_state.substances), t - cost, c + cost))
	return None


def apply_all_actions(state, height, time, reward, cost):
	if height <= 0 or time <= 0 or state.is_final_state():
		return [reward, HEIGHT - height, cost] #TODO change 4 !
	max_reward = 0
	best_action = None
	steps = 999
	total_cost = 999
	if state.can_clean() or state.can_refill():
		return [reward, HEIGHT - height, cost]
	if state.can_move():
		for (dest, costt) in state.move_options():
			new_state = deepcopy(state)
			[t, r] = apply_action(new_state, time, reward, (MOVE, dest, costt))
			[r, s, c] = apply_all_actions(new_state, height - 1, t, r, cost + costt)
			if c < total_cost:
				max_reward = r
				steps = s
				best_action = (MOVE, dest, costt)
				total_cost = c

	return [max_reward, steps, total_cost]


def construct_action(action, old_location, location):
	if action[0] == MOVE:
		return 'Move(' + str(old_location) + ',' + str(action[1]) + ')'
	elif action == REFILL:
		return 'Refill(' + str(location) + ')'
	elif action == CLEAN:
		return 'Clean(' + str(location) + ')'

def get_action_name(value):
	return value.split('(')[0]

def get_action_args(value):
	i = value.find('(')
	return value[i + 1:-1].split(',')

def read_environment(filename):
	global Capacity, Time, graph, Reward, Rooms

	graph = {}
	Capacity = 0
	Rooms = []
	Time = 0
	Reward = 0

	f = open(filename, 'r')
	line = f.readline()
	values = line.split()
	X = int(values[0])
	T = int(values[1])
	S = int(values[2])
	C = int(values[3])
	M = int(values[4])
	N = int(values[5])
	P = int(values[6])
	crtIndex = int(values[7])

	state = State(crtIndex)
	Time = int(T)
	Capacity = C
	
	for i in range(S):
		state.carries(i, Capacity)

	for i in range(N + M):
		Rooms.append(Room(i))

	line = f.readline()
	values = line.split()
	for i in values:
		Rooms[int(i)].set_roomtype(WAREHOUSE)

	for i in range(int(P)):
		line = f.readline()
		values = line.split()
		n1 = int(values[0])
		n2 = int(values[1])
		cost = int(values[2])
		if n1 in graph:
			graph[n1].append((n2, cost))
		else:
			graph[n1] = [(n2, cost)]
		if n2 in graph:
			graph[n2].append((n1, cost))
		else:
			graph[n2] = [(n1, cost)]


	for i in range(N):
		line = f.readline()
		values = line.split()
		index = int(values[0])
		dirty = int(values[1])
		dim = int(values[2])
		nr_subst = int(values[3])

		Rooms[index].set_dimension(dim)

		if dirty == 1:
			state.add_dirty_room(index)

		for j in range(4, 4 + 2 * nr_subst, 2):
			Rooms[index].add_substance(int(values[j]), int(values[j+1]))

	#print(graph)
	#for room in Rooms:
	#	print(room)
	return state


def main(argv):
    print(makeplan('tests\sample.in'))

if __name__ == '__main__':
    main(sys.argv)
