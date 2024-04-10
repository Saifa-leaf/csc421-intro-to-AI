def isComplete(assignment):
    return None not in (assignment.values())

def select_unassigned_variable(variables, assignment):
    for var in variables:
        if assignment[var] is None:
            return var

def is_consistent(assignment, constraints):
    for constraint_violated in constraints:
        if constraint_violated(assignment):
          return False
    return True

def init_assignment(csp):
    assignment = {}
    for var in csp["VARIABLES"]:
        assignment[var] = None
    return assignment

def add_constraint(csp, constraint): 
    csp['CONSTRAINTS'].append(constraint)
    
def recursive_backtracking(assignment, csp):
    if isComplete(assignment):
        return assignment
    var = select_unassigned_variable(csp["VARIABLES"], assignment)
    for value in csp["DOMAINS"]:
        assignment[var] = value
        if is_consistent(assignment, csp["CONSTRAINTS"]):
            result = recursive_backtracking(assignment, csp)
            if result != "FAILURE":
                return result
        assignment[var] = None
    return "FAILURE"


def binary_constraint(valGet, valToAssign, violations):
    return lambda asmt: (asmt[valToAssign], asmt[valGet]) in violations
  
# add your code for CSP-based type inference as described in the notebook 
# below. The answer to the problem provided should be named result and 
# be a dictionary with a complete assignment of the variables to types 
# as returned by the CSP backtracking method. 
def unary_constraint(var, violations):
    return lambda asmt: asmt[var] in violations

def ternary_constraint(sum_var, var1, var2, violations):
    return lambda asmt: (asmt[sum_var], asmt[var1], asmt[var2]) in violations

csp1 = {"VARIABLES": ["I", "F", "X", "Y", "Z", "W"],
        "DOMAINS": ["int", "float"],
        "CONSTRAINTS": []}
violations = {("int", "float"), ("int", "float", "float"), ("int", "float", "int"), ("int", "int", "float")}

add_constraint(csp1, unary_constraint('I', ['float']))
add_constraint(csp1, unary_constraint('F', ['int']))
add_constraint(csp1, binary_constraint("X","I", violations))
add_constraint(csp1, ternary_constraint("Y", "X", "F", violations))
add_constraint(csp1, ternary_constraint("Z", "X", "Y", violations))
add_constraint(csp1, ternary_constraint("W", "X", "I", violations))




result = recursive_backtracking(init_assignment(csp1), csp1)    





# def unary_constraint(var, violations):
#     return lambda asmt: asmt[var] in violations

# def binary_constraint(valGet, valToAssign, violations):
#     return lambda asmt: (asmt[valToAssign], asmt[valGet]) in violations

# def ternary_constraint(sum_var, var1, var2, violations):
#     return lambda asmt: (asmt[sum_var], asmt[var1], asmt[var2]) in violations

# csp1 = {"VARIABLES": ["I", "F", "X", "Y", "Z", "W"],
#         "DOMAINS": ["int", "float"],
#         "CONSTRAINTS": []}

# violations = {("int", "float"), ("int", "float", "float"), ("int", "float", "int"), ("int", "int", "float")}

# add_constraint(csp1, unary_constraint('I', ['float']))
# add_constraint(csp1, unary_constraint('F', ['int']))
# add_constraint(csp1, binary_constraint("X","I", violations))
# add_constraint(csp1, ternary_constraint("Y", "X", "F", violations))
# add_constraint(csp1, ternary_constraint("Z", "X", "Y", violations))
# add_constraint(csp1, ternary_constraint("W", "X", "I", violations))

