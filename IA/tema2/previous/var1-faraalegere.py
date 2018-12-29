import sys
from copy import deepcopy
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
math_predicates = ['isBigger', 'equal', 'sum', 'dif']

state = []
newState = []
reward = 0
Time = -1
# (action_name, [preconditions], [repetitive preconditions], [LA], [LE])
actions = [
	('Move', [make_var('r1'), make_var('r2')], 
		[make_atom('location', make_var('r1')), make_atom('edge', make_var('r1'), make_var('r2'), make_var('cost'))], 
		[],
		[make_atom('location', make_var('r2'))], 
		[make_atom('location', make_var('r1'))]),
	('Clean', [make_var('r')], 
		[make_atom('location', make_var('r')), make_atom('isRoom', make_var('r')),
		make_atom('isDirty', make_var('r'))],
		[make_atom('substance', make_var('r'), make_var('s'), make_var('n')),
		make_atom('carries', make_var('s'), make_var('m')), make_atom('isBigger', make_var('m'), make_var('n')),
		make_atom('dif', make_var('m'), make_var('n'), make_var('d'))],
		[make_atom('carries', make_var('s'), make_var('d'))],
		[make_atom('isDirty', make_var('r')), make_atom('carries', make_var('s'), make_var('m'))]),
	('Refill', [make_var('w')], 
		[make_atom('location', make_var('w')), make_atom('isWarehouse', make_var('w')), make_atom('capacity', make_var('n'))],
		[make_atom('carries', make_var('s'), make_var('m'))],
		[make_atom('carries', make_var('s'), make_var('n'))],
		[make_atom('carries', make_var('s'), make_var('m'))])
]

def makeplan(filename):
    # TODO
    read_environment(filename)
    path = []
    return forward(path)

def forward(path):
	if len(env['isDirty']) == 0:
		return path
	#search actions with satisfied preconditions
	availableActions = []
	for action in actions:
		if preconditionsSatisfied(action[2]):
			availableActions.append(action)
	print("AVAILABLE ACTIONS")
	print([a[0] for a in availableActions])
	
	if len(availableActions) == 0:
		return []
	#choose best action #TODO
	A = availableActions[0]

	#applyAction(A)

#def findBestAction(availableActions):


def applyAction(action):
	global newState, state

	#Time = Time - actionCost(action)
	newState = deepcopy(state)
	findAllSubstitutions(action, action[2], {})
	#print("oldState " + str(state))
	#print("newState " + str(newState))
	state = newState
	newState = []


def findAllSubstitutions(action, atoms, subst):
	if not atoms:
		print(subst)
		applyLE(action, subst)
		applyLA(action, subst)
		return

	atom = atoms[0]
	name = get_head(atom)
	if name in env:
		facts = env[name]
	elif name in math_predicates:
		return findAllSubstitutions(action, atoms[1:], subst)
	else:
		facts = state

	for fact in facts:
		newSubst = unify(atom, fact)
		if newSubst != False and newSubst != None:
			copySubst = deepcopy(subst)
			copySubst.update(newSubst)

			remaining = deepcopy(atoms[1:])
			for i in range(len(remaining)):
				remaining[i] = substitute(remaining[i], newSubst)
			findAllSubstitutions(action, remaining, copySubst)
			
def applyLE(action, subst):
	global newState
	LE = action[4]
	for e in LE:
		e = substitute(e, subst)
		name = get_head(e)
		if e in newState:
			#print("found atom to remove " + str(e))
			newState.remove(e)

def applyLA(action, subst):
	global newState
	LA = action[3]
	for a in LA:
		a = substitute(a, subst)
		name = get_head(a)
		if name not in env and name not in math_predicates:
			if a not in newState:
				newState.append(a)


# check if the preconditions are satisfiable
def preconditionsSatisfied(atoms):
	atom = atoms[0]
	#print("checking " + str(atom))
	name = get_head(atom)
	if name in env:
		#print("NAME IN ENV")
		facts = env[name]
	elif name in math_predicates:
		res = checkMathPredicates(name, atom)
		if res == True and len(atoms) == 1:
			return True
		elif res == True:
			return preconditionsSatisfied(atoms[1:])
		else:
			return False
	else:
		facts = state

	#print(facts)
	hasUnified = False

	for fact in facts:
		s = unify(atom, fact)
		#print("with " + str(fact) + " unify is " + str(s))
		if s != False and s != None:
			hasUnified = True
			#print("unify " + str(atom) + " with " + str(fact) + " under ")
			#print(s)
			if len(atoms) == 1:
				return True

			remaining = deepcopy(atoms[1:])
			for i in range(len(remaining)):
				remaining[i] = substitute(remaining[i], s)
			#print("remaining " + str(remaining))
			res = preconditionsSatisfied(remaining)
			if res == False:
				return False

	if hasUnified:
		return True
	return False

def checkMathPredicates(name, atom):
	args = get_args(atom)
	if is_variable(args[0]) or is_variable(args[1]):
		return False
	a = get_value(args[0])
	b = get_value(args[1])
	if name == 'isBigger':
		return a >= b
	elif name == 'equal':
		return a == b
	elif name == 'sum':
		if is_constant(args[2]) and (a + b == get_value(args[2])):
			return True
		elif is_variable(args[2]):
			args[2] = substitute(args[2], {get_name(args[2]): make_const(a + b)})
			return True
	elif name == 'dif':
		if is_constant(args[2]) and (a - b == get_value(args[2])):
			return True
		elif is_variable(args[2]):
			args[2] = substitute(args[2], {get_name(args[2]): make_const(a - b)})
			return True
	return False



def read_environment(filename):
	global env, state, time
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
	env['capacity'].append(make_atom('capacity', make_const(C)))
	state.append(make_atom('location', make_const(crtIndex)))

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
		for j in range(4, 4 + 2 * nr_subst, 2):
			env['substance'].append(make_atom('substance', make_const(index), make_const(int(values[j])), make_const(int(values[j+1]))))




def main(argv):
    #print(makeplan(FILENAME))
    print(makeplan('sample.in'))

if __name__ == '__main__':
    main(sys.argv)

