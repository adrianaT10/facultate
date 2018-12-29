
# coding: utf-8


from operator import add

def eq_s(s1, s2):
    if isinstance(s1, dict) and isinstance(s2, dict):
        return len(s1) == len(s2) and not [v for v in s1 if v not in s2 or s1[v] != s2[v]]
    return s1 == s2
def pf(f, environment, evaluateF = True):
    if evaluateF:
        return eval("print_formula("+f+", True)", environment)
    else:
        return eval("print_formula(f, True)", environment, {"f": f})
def ps(s, environment):
    if s == False:
        return "False"
    return "{" + ", ".join([(v + " -> " + pf(s[v], environment, False)) for v in s]) + "}"
def pTest(index, result, returned, check, test = None, printValue = False):
    out = "Test " + str(index) + ": "
    if result:
        out += "OK" 
        if printValue:
            out += ", got <" + str(returned) + ">"
    else:
        out += "Failed, got <" + str(returned) + ">, should be <" + str(check) + ">."
    if not result and test:
        out += " Test was <" + str(test) + ">."
    print(out)

def test(v, c, environment, idx):
    value = eval(v, environment)
    result = value == c
    pTest(idx, result, value, c, v)
    return result

def testC(v, c, conds, environment, idx):
    for cond in conds:
        if cond[0] == 'True':
            condition = eval(cond[1], environment)
        elif cond[0] == 'MinLenList':
            lst = eval(cond[2], environment)
            condition = isinstance(lst, list) and len(lst) >= cond[1]
        elif cond[0] == 'instance':
            condition = eval(cond[2], environment) and isinstance(eval(cond[2], environment), cond[1])
        else:
            print("Condition type", cond[0], "missing for test", idx)
            return False
        if not condition:
            print("Test", idx, ":", cond[-1], ". Test was <" + str(v) + ">.")
            return False
    return test(v, c, environment, idx)

def testForm(v, c, environment, idx):
    value = eval(v, environment)
    check = eval(c, environment)
    Pvalue = pf(v, environment)
    Pcheck = pf(c, environment)
    result = value == check
    pTest(idx, result, Pvalue, Pcheck, v)
    return result

def testOccur(f1, f2, si, check, environment, idx):
    value = eval("occur_check("+f1+","+f2+","+si+")", environment)
    initial = eval(si, environment)
    result = value == check
    Ptest = "occur_check " + pf(f1, environment) + " in " + pf(f2, environment) + \
            ((" under " + ps(initial, environment)) if initial else "")
    pTest(idx, result, value, check, Ptest)
    return result

def testUnify(f1, f2, si, sc, environment, idx):
    value = eval("unify("+f1+","+f2+","+si+")", environment)
    check = eval(sc, environment)
    initial = eval(si, environment)
    Ptest = "unify " + pf(f1, environment) + " with " + pf(f2, environment) + \
            ((" under " + ps(initial, environment)) if initial else "")
    Pvalue = ps(value, environment)
    Pcheck = ps(check, environment)
    result = eq_s(value, check)
    pTest(idx, result, Pvalue, Pcheck, Ptest, True)
    return result

def testResolves(f1, f2, sc, environment, idx):
    value = eval("resolves("+f1+","+f2+")", environment)
    Ptest = "resolves " + pf(f1, environment) + " with " + pf(f2, environment)
    if sc and value and isinstance(value, tuple) and len(value) > 2:
        (l1, l2, sv) = value
        Pvalue = "(" + pf(l1, environment, False) + ", " + pf(l2, environment, False) + ", " + ps(sv, environment)
        scA = {}
        for v in sc:
            scA[v] = eval(sc[v], environment)
        sc = scA
        result = eq_s(sv, sc)
    elif sc == False:
        Pvalue = value
        result = not value
    else:
        print("Test " + str(idx) + " : Result should be a 3-tuple, was <" + str(value) + ">")
        return False
    Pcheck = ps(sc, environment)
    pTest(idx, result, Pvalue, Pcheck, Ptest, True)
    return result

def test_batch(index, environment = None):
    print(">>> Test batch [" + str(index) + "]")
    idx = 0
    succeeded = 0
    for batch in testBatch[index]:
        (f, tests) = batch
        for test in tests:
            succeeded += 1 if f(*(list(test) + [environment, idx])) else 0
            idx += 1
    print(">>> ", succeeded, "/", idx, "tests successful.")
    return


testBatch = {}

# sanity check
testBatch['sanity'] = [(test, [
            ("True", True),
            ("False", False),
            ("False", True),  # fails
            ("True", False),  # fails
            ("5+3", 8),
            ("add(5,3)", 8),
        ]),
                      (testC, [
            ("True", True, [("True", "True", "This if false.")]),
            ("True", False, [("True", "True", "This if false.")]),  # fails
            ("True", True, [("True", "False", "This if false.")]),  # fails condition
            ("True", True, [("instance", list, "[1, 2]", "Is not list,")]),
            ("True", True, [("instance", list, "[]", "Is None or not list,")]),  # fails condition
            ("True", True, [("instance", list, "(1, 2)", "Is not list,")]),  # fails condition
        ])]
#test_batch('sanity')




args_replaced = "get_args(replace_args(make_and(make_atom('P', make_var('x')), make_atom('Q', make_var('x'))), " +                         "[make_atom('P', make_const(1)), make_atom('Q', make_const(1))]))"
args_2 = "get_args(make_and(make_atom('P', make_var('X')), make_atom('Q', make_const('5'))))"
args_3 = "get_args(make_and(make_atom('P', make_var('X')), make_atom('Q', make_var('Y')), make_atom('T', make_var('Z'))))"
args_1 = "get_args(replace_args(make_atom('P', make_var('X')), [make_const(2)]))"
testBatch[0] = [(test, [
            # 0
            ("is_term(make_const('A'))", True),
            ("is_term(make_var('x'))", True),
            ("is_atom(make_var('x'))", False),
            ("is_term(make_function_call(add, make_const(2), make_var('x')))", True),
            ("is_atom(make_function_call(add, make_const(2), make_var('x')))", False),
            # 5
            ("is_sentence(make_function_call(add, make_const(2), make_var('x')))", False),
            ("is_atom(make_atom('P', make_var('x')))", True),
            ("is_term(make_atom('P', make_var('x')))", False),
            ("is_sentence(make_neg(make_atom('P', make_var('x'))))", True),
            ("is_atom(make_neg(make_atom('P', make_var('x'))))", False),
            # 10
            ("get_value(make_const(2))", 2),
            ("get_name(make_var('X'))", 'X'),
            ("get_name(make_atom('P'))", None),
            ("get_head(make_atom('P'))", 'P'),
            ("get_head(make_function_call(add, make_const(2), make_var('x')))", str(add)),
        ]),
                (testC, [
            # 15
            ("is_atom("+args_2+"[0])", True, \
                [("MinLenList", 2, args_2, "N/A. Get args returns a list that is shorter than 2.")]),
            ("is_atom("+args_2+"[1])", True, \
                [("MinLenList", 2, args_2, "N/A. Get args returns a list that is shorter than 2.")]),
            ("is_atom("+args_3+"[2])", True, \
                [("MinLenList", 3, args_3, "N/A. Get args returns a list that is shorter than 2.")]),
            ("is_variable(get_args("+args_2+"[0])[0])", True, \
                [("MinLenList", 2, args_2, "N/A. Get args returns a list that is shorter than 2.")]),
            ("is_constant(get_args("+args_2+"[1])[0])", True, \
                [("MinLenList", 2, args_2, "N/A. Get args returns a list that is shorter than 2.")]),
            ("get_name(get_args(make_atom('P', make_var('X')))[0])", 'X', \
                [("MinLenList", 1, "get_args(make_atom('P', make_var('X')))")]),
            ("is_constant("+args_1+"[0])", True, [("MinLenList", 1, args_1)]),
            ("get_value("+args_1+"[0])", 2, [("MinLenList", 1, args_1)]),
            ("get_value(get_args("+args_replaced+"[0])[0])", 1, \
                [("MinLenList", 1, args_replaced, "N/A. Replaced arguments not a list.")]),
        ])]


testBatch[1] = [(testForm, [
            ("substitute(formula1, {'x': make_const(5)})", "test_formula(5)"),
            ("substitute(formula1, {'x': make_var('z'), 'z': make_const(7)})", "test_formula(7)"),
            ("substitute(formula1, {'z': make_const(7), 'x': make_var('z')})", "test_formula(7)"),
            ("substitute(formula1, {'x': make_const(5)})", "test_formula(5)"),
            ("substitute(formula1, {'y': make_function_call(add, make_var('x'), make_const(2)), 'x': make_const(1)})",
                "test_formula(1, True)"),
        ])]

testBatch[2] = [(testOccur, [
            ("make_var('x')", "make_const(5)", "{}", False), #0
            ("make_var('x')", "make_var('y')", "{}", False), #1
            ("make_var('x')", "make_function_call(add, make_var('x'))", "{}", True), #2
            ("make_var('y')", "make_function_call(add, make_var('x'))", "{'x': make_var('y')}", True), #3
            ("make_var('z')", "make_function_call(add, make_var('x'))", \
                                      "{'x': make_var('y'), 'y': make_var('z')}", True), #4
            ("make_var('z')", "make_function_call(add, make_const(5), make_function_call(add, make_var('x')))", \
                                      "{'x': make_var('y'), 'y': make_var('z')}", True), #5
            ("make_var('z')", "make_function_call(add, make_var('w'))",
                                      "{'x': make_var('y'), 'y': make_var('z')}", False), #6
        ])]

testBatch[3] = [(testUnify, [
            ("make_atom('P', make_const('B'))", "make_atom('P', make_const('A'))", "{}", "False"),
            #1 # P(x) vs P(A) -> x: A
            ("make_atom('P', make_var('x'))", "make_atom('P', make_const('A'))", "{}", "{'x': make_const('A')}"),
            #2 # P(x, x) vs P(A, A) -> x: A
            ("make_atom('P', make_var('x'), make_var('x'))", "make_atom('P', make_const('A'), make_const('A'))", "{}",
                          "{'x': make_const('A')}"),
            #3 # P(x, A) vs P(A, x) -> x: A
            ("make_atom('P', make_var('x'), make_const('A'))", "make_atom('P', make_const('A'), make_var('x'))", "{}",
                          "{'x': make_const('A')}"),
            #4 # P(x, A, x) vs P(A, x, A) -> x: A
            ("make_atom('P', make_var('x'), make_const('A'), make_var('x'))", 
                             "make_atom('P', make_const('A'), make_var('x'), make_const('A'))", "{}",
                             "{'x': make_const('A')}"),
            #5 # P(x) vs P(add[Z, 5]) -> x: add[Z, 5]
            ("make_atom('P', make_var('x'))", "make_atom('P', make_function_call(add, make_var('Z'), make_const(5)))", "{}",
                                "{'x': make_function_call(add, make_var('Z'), make_const(5))}"),
            #6 # P(x, y, z) vs P(A, B, C) -> x: A, y: B, z: C
            ("make_atom('P', make_var('x'), make_var('y'), make_var('z'))", 
                            "make_atom('P', make_const('A'), make_const('B'), make_const('C'))", "{}",
                            "{'z': make_const('C'), 'y': make_const('B'), 'x': make_const('A')}"),
            #7 # Q(2, 3, add[x, y]) vs Q(x, y, add[2, 3]) -> x: 2, y: 3
            ("make_atom('Q', make_const(2), make_const(3), make_function_call(add, make_var('x'), make_var('y')))",
                            "make_atom('Q', make_var('x'), make_var('y'), make_function_call(add, make_const(2), make_const(3)))",
                            "{}", "{'x': make_const(2), 'y': make_const(3)}"),
            #8 # P(x, y) vs P(x, add[y, 2]) -> false
            ("make_atom('P', make_var('x'), make_var('y'))", 
                         "make_atom('P', make_const('x'), make_function_call(add, make_var('y'), make_const(2)))", "{}",
                         "False"),
            #9 # P(B) vs Q(B) -> False
            ("make_atom('P', make_const('B'))", "make_atom('Q', make_const('B'))", "{}", "False"),
        ])]
  

testBatch[4] = [(testResolves, [
            #0
            ("KB_America[1]", "KB_America[6]", {'v2': "make_const('General_Awesome')"}),
            ("KB_America[5]", "KB_America[8]", {'v8': "make_const('M1')", 'v9': "make_const('Nono')"}),
            ("KB_America[9]", "KB_America[6]", {'v16': "make_var('v2')"}),
            ("KB_America[3]", "KB_America[10]", {'v18': "make_const('Nono')"}),
            #4
            ("KB_America[0]", "KB_America[1]", False),
            ("KB_America[2]", "KB_America[10]", False),
            ("KB_America[2]", "KB_America[2]", False),
            ("KB_America[6]", "KB_America[6]", False),
    ])]


