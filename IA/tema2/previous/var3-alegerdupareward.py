import sys
from copy import deepcopy
from random import randint
from Lab05 import make_atom, make_const, make_var, get_head, unify, substitute, print_formula, get_value, get_args, is_variable, is_constant, get_name

FILENAME = 'sample.in'

env = {
	'dimension': [],
	'substance': [],
	'isDirty': [],
	'edge': [],
	'isRoom': [],
	'isWarehouse': [],
	'capacity': []
}
math_predicates = ['isBigger', 'isSmaller', 'equal', 'sum', 'dif']

state = []
#newState = []
reward = 0
time = -1
# (action_name, [preconditions], [repetitive preconditions], [LA], [LE])
actions = [
	('Move', [make_var('r1'), make_var('r2')], 
		[make_atom('location', make_var('r1')), make_atom('edge', make_var('r1'), make_var('r2'), make_var('cost'))], 
		[],
		[make_atom('location', make_var('r2'))], 
		[make_atom('location', make_var('r1'))]),
	('Clean', [make_var('r')], 
		[make_atom('location', make_var('r')), make_atom('isRoom', make_var('r')),
		make_atom('isDirty', make_var('r')), make_atom('dimension', make_var('r'), make_var('dim'))],
		[make_atom('substance', make_var('r'), make_var('s'), make_var('n')),
		make_atom('carries', make_var('s'), make_var('m')), make_atom('isBigger', make_var('m'), make_var('n')),
		make_atom('dif', make_var('m'), make_var('n'), make_var('d'))],
		[make_atom('carries', make_var('s'), make_var('d'))],
		[make_atom('isDirty', make_var('r')), make_atom('carries', make_var('s'), make_var('m'))]),
	('Refill', [make_var('w')], 
		[make_atom('location', make_var('w')), make_atom('isWarehouse', make_var('w')), 
		make_atom('capacity', make_var('n')), make_atom('carries', make_var('sprim'), make_var('mprim')),
		make_atom('isSmaller', make_var('mprim'), make_var('n'))],
		[make_atom('carries', make_var('s'), make_var('m'))],
		[make_atom('carries', make_var('s'), make_var('n'))],
		[make_atom('carries', make_var('s'), make_var('m'))])
]

def makeplan(filename):
    # TODO
    read_environment(filename)
    path = []
    path =  forward(path)
    #print("FINAL PATH " + str(path))
    #print('REWARD ' + str(reward))
    return path

def forward(path):
	global state, time, reward
	if len(env['isDirty']) == 0 or time <= 0:
		return path
	#search actions with satisfied preconditions
	availableActions = findAvailableActions(state)

	#print("AVAILABLE ACTIONS")
	#print(availableActions.keys())
	#print(availableActions)
	
	if len(availableActions) == 0:
		return path

	#choose best action #TODO
	[actionName, index, cost, rew] = findBestAction(availableActions, path)
	#TODO should be removed
	if actionName == None:
		print ("NO OTHER ACTION")
		return path
	if time <= 0:
		return path

	A = [a for a in actions if a[0] == actionName][0]

	print("APPLY ACTION " + actionName)
	#print("APPLY SUBST " + str(availableActions[actionName][index]))
	state = applyAction(A, availableActions[actionName][index])
	time = time - cost
	reward = reward + rew
	print("TIME " + str(time))
	print("REWARD " + str(reward))
	
	path.append(constructAction(availableActions, A, index))

	return forward(path)


def findAvailableActions(state):
	availableActions = {}
	for action in actions:
		allSubst = []
		findSubstitutions(action, action[2], {}, allSubst, state)

		if not allSubst:
			continue
		for subst in allSubst:
				repetitive = []
				for i in range(len(action[3])):
					repetitive.append(substitute(action[3][i], subst))
				allSubstRepetitive = []
				res = findSubstitutions(action, repetitive, {}, allSubstRepetitive, state)
				#print("repetitive subst " + str(allSubstRepetitive))
				#print("are all unifing " + str(res))
				if res == False:
					continue
				if action[0] in availableActions:
					availableActions[action[0]].append((subst, allSubstRepetitive))
				else:
					availableActions[action[0]] = [(subst, allSubstRepetitive)]

	return availableActions


def constructAction(availableActions, action, index):
	newElem = action[0] + '('
	for arg in action[1]:
		arg = substitute(arg, availableActions[action[0]][index][0])
		newElem = newElem + str(get_value(arg)) + ','
	newElem = newElem[:-1] + ')'
	return newElem

# Returns [action_name, index of subst in the list of subtitutions for that action, cost, reward]
def findBestAction(availableActions, path):
	# TODO
	global state, time
	cost = 0
	if 'Clean' in availableActions.keys():
		cost = get_value(availableActions['Clean'][0][0]['dim'])
		return ['Clean', 0, cost, cost]
	if 'Refill' in availableActions.keys():
		return ['Refill', 0, 1, 0]
	if 'Move' in availableActions.keys():
		substIndex = 0
		maxReward = -1
		cost = -1
		for subst in availableActions['Move']:
			moveCost = get_value(subst[0]['cost'])
			print('move cost ' + str(moveCost) + " time " + str(time))
			if moveCost > time:
				continue
			index = availableActions['Move'].index(subst)
			if len(path) >= 1 and getActionName(path[len(path) - 1]) == 'Move':
				args = getActionArgs(path[-1])
				#print("ARGS "  + str(args))
				if int(args[0]) == get_value(subst[0]['r2']) and len(availableActions['Move']) > 1:
					continue
			#TODO apply action
			# nu merge applyaction pentru ca ar modifica si env; asa schimb manual doar locatia
			#newState = applyAction(actions[0], subst)
			newState = deepcopy(state)
			for atom in newState:
				if get_head(atom) == 'location':
					newState.remove(atom)
					break
			newState.append(make_atom('location', make_const(get_value(subst[0]['r2']))))
			#TODO see available actions for the new states
			newAvailableActions = findAvailableActions(newState)
			print(newAvailableActions.keys())
			#TODO pick the best move
			if 'Clean' in newAvailableActions:
				cleanCost =  get_value(newAvailableActions['Clean'][0][0]['dim'])
				print("Clean cost " + str(cleanCost) + " max reward so far " + str(maxReward))
				if 1000 + cleanCost - moveCost > maxReward and moveCost + cleanCost <= time:
					maxReward =  1000 + cleanCost - moveCost
					substIndex = index
					cost = moveCost
			if 'Refill' in newAvailableActions:
				print("Refill" + " max reward so far " + str(maxReward))
				if 50 - moveCost > maxReward:
					maxReward = 50 - moveCost
					substIndex = index
					cost = moveCost
			# if 'Move' in newAvailableActions and len(newAvailableActions['Move']) > 1: # daca nu e dead end
			# 	if 0 > maxReward:
			# 		maxReward = 0
			# 		substIndex = index
			# 		cost = moveCost
		print("chosen cost " + str(cost))
		if cost != -1:
			return ['Move', substIndex, cost, 0]
		else:
			substIndex = 0
			minCost = 9999
			for subst in availableActions['Move']:
				moveCost = get_value(subst[0]['cost'])
				if moveCost > time:
					continue
				index = availableActions['Move'].index(subst)
				if len(path) >= 1 and getActionName(path[len(path) - 1]) == 'Move':
					args = getActionArgs(path[-1])
					#print("ARGS "  + str(args))
					if int(args[0]) == get_value(subst[0]['r2']) and len(availableActions['Move']) > 1:
						continue
				if moveCost < minCost:
					substIndex = index
					minCost = moveCost
			print("new chosen cost " + str(minCost))
			return ['Move', substIndex, minCost, 0]

	return [None, None, 0, 0]

def getActionName(value):
	return value.split('(')[0]

def getActionArgs(value):
	i = value.find('(')
	return value[i + 1:-1].split(',')

def applyAction(action, substitution):
	global state

	newState = deepcopy(state)
	newState = applyLE(action, substitution, newState)
	newState = applyLA(action, substitution, newState)

	#print("")
	#print("APPLY ACTION " + str(action[0]))
	#print("SUBTITUTION " + str(substitution))
	#print("OLD STATE ")
	#print_state(state)
	#print("NEW STATE ")
	#print_state(newState)
	return newState

# True daca au unificat toate predicatele; allSubst -> lista cu substitutiile
def findSubstitutions(action, atoms, subst, allSubst, state):
	if not atoms:
		#print("found subst " + str(subst))
		if len(subst) != 0:
			allSubst.append(subst)
		return True

	atom = atoms[0]
	name = get_head(atom)
	if name in env:
		facts = env[name]
	elif name in math_predicates:
		newSubst = {}
		res = checkMathPredicates(name, atom, newSubst)
		if res == False:
			return False
		else:
			if newSubst != {}:
				#TODO update the remaining with the newSubst?
				subst.update(newSubst)
			return findSubstitutions(action, atoms[1:], subst, allSubst, state)
	else:
		facts = state

	hasUnifiedWithAll = True

	for fact in facts:
		#TODO pot sa aplic newSubst in unify si sa nu mai fac remaining?
		newSubst = unify(atom, fact)
		if newSubst != False and newSubst != None:
			copySubst = deepcopy(subst)
			copySubst.update(newSubst)

			remaining = deepcopy(atoms[1:])
			for i in range(len(remaining)):
				remaining[i] = substitute(remaining[i], newSubst)
			res = findSubstitutions(action, remaining, copySubst, allSubst, state)
			if not res:
				hasUnifiedWithAll = False

	return hasUnifiedWithAll

			
def applyLE(action, substitution, newState):
	LE = deepcopy(action[5])
	subst = substitution[0]
	for i in range(len(LE)):
		LE[i] = substitute(LE[i], subst)
		name = get_head(LE[i])
		if name == 'isDirty':
			env['isDirty'].remove(LE[i])
		if LE[i] in newState:
			#print("found atom to remove " + str(e))
			newState.remove(LE[i])

	for subst in substitution[1]:
		for e in LE:
			e = substitute(e, subst)
			name = get_head(e)
			if e in newState:
				#print("found atom to remove " + str(e))
				newState.remove(e)
	return newState

def applyLA(action, substitution, newState):
	LA = deepcopy(action[4])
	subst = substitution[0]

	for i in range(len(LA)):
		LA[i] = substitute(LA[i], subst)
		name = get_head(LA[i])
		if not substitution[1] and name not in env and name not in math_predicates:
			if LA[i] not in newState:
				newState.append(LA[i])
	for subst in substitution[1]:
		for a in LA:
			a = substitute(a, subst)
			name = get_head(a)
			if name not in env and name not in math_predicates:
				if a not in newState:
					newState.append(a)
	return newState

def print_state(stare):
	for atom in stare:
		print_formula(atom)


def checkMathPredicates(name, atom, subst = None):
	args = get_args(atom)
	if is_variable(args[0]) or is_variable(args[1]):
		return False
	a = get_value(args[0])
	b = get_value(args[1])
	if name == 'isBigger':
		return a >= b
	elif name == 'isSmaller':
		return a < b
	elif name == 'equal':
		return a == b
	elif name == 'sum':
		if is_constant(args[2]) and (a + b == get_value(args[2])):
			return True
		elif is_variable(args[2]):
			subst[get_name(args[2])] = make_const(a + b)
			return True
	elif name == 'dif':
		if is_constant(args[2]) and (a - b == get_value(args[2])):
			return True
		elif is_variable(args[2]):
			subst[get_name(args[2])] = make_const(a - b)
			return True
	return False



def read_environment(filename):
	global env, state, time, readBefore
	env = {
	'dimension': [],
	'substance': [],
	'isDirty': [],
	'edge': [],
	'isRoom': [],
	'isWarehouse': [],
	'capacity': []
	}

	dirtyValue = 0
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

	time = int(T)
	for a in state:
		if a[0] == 'location':
			state.remove(a)
			break
	state.append(make_atom('location', make_const(crtIndex)))
				
	env['capacity'].append(make_atom('capacity', make_const(C)))
	
	for i in range(S):
		state.append(make_atom('carries', make_const(i), make_const(C)))

	line = f.readline()
	values = line.split()
	for i in values:
		env['isWarehouse'].append(make_atom('isWarehouse', make_const(int(i))))

	for i in range(int(P)):
		line = f.readline()
		values = line.split()
		env['edge'].append(make_atom('edge', make_const(int(values[0])), make_const(int(values[1])), make_const(int(values[2]))))
		env['edge'].append(make_atom('edge', make_const(int(values[1])), make_const(int(values[0])), make_const(int(values[2]))))
	
	env['isDirty'] = []
	for i in range(int(N)):
		line = f.readline()
		values = line.split()
		index = int(values[0])
		dirty = int(values[1])
		dim = int(values[2])
		nr_subst = int(values[3])
		env['isRoom'].append(make_atom('isRoom', make_const(index)))
		env['dimension'].append(make_atom('dimension', make_const(index), make_const(dim)))
		if dirty == 1:
			env['isDirty'].append(make_atom('isDirty', make_const(index)))
			dirtyValue = dirtyValue + dim
		for j in range(4, 4 + 2 * nr_subst, 2):
			env['substance'].append(make_atom('substance', make_const(index), make_const(int(values[j])), make_const(int(values[j+1]))))

	print("Reward daca se curata toate camerele " + str(dirtyValue))

def main(argv):
    #print(makeplan(FILENAME))
    print(makeplan('sample.in'))

if __name__ == '__main__':
    main(sys.argv)
