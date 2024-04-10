
# Add the code for this function as described in the notebook 
def evaluate(s):
    list_exp = s.split(' ')
    result = True
    
    if (list_exp[0] == '&'): 
        result = list_exp[1] == list_exp[2] and list_exp[1] == '1'
    elif (list_exp[0] == '=>'):
        result = list_exp[1] != '1' or list_exp[2] != '0'
    elif (list_exp[0] == '|'):
        result = (list_exp[1] == '1' or list_exp[2] == '1')
    else:
        result = list_exp[1] == list_exp[2]
    
    if (result):
        return 1
    else:
        return 0


# Examples test cases
e1 = "| 0 1"
e2 = "<=> 1 1"
e3 = "& 0 0"

res_e1 = evaluate(e1)
res_e2 = evaluate(e2)
res_e3 = evaluate(e3)


print(f'{e1} = {res_e1}')
print(f'{e2} = {res_e2}')
print(f'{e3} = {res_e3}')

d = {'foo': 0, 'b': 1}
print(d)
be1 = '& 0 1'
be2 = '& foo 1'
be3 = '& foo ~b'


# Add the code for this function 
def evaluate_with_bindings(s,d):
    list_exp = s.split(' ')
    result = True
    newDict = {}
    
    for key in d:
        if (d[key] == 0 and key[:1] != '~'):
            newDict['~' + key] = '1'
        elif (d[key] == 1 and key[:1] != '~'):
            newDict['~' + key] = '0'
        elif (d[key] == 0 and key[:1] == '~'):
            newDict[key[1:]] = '1'
        elif (d[key] == 1 and key[:1] == '~'):
            newDict[key[1:]] = '0'
        newDict[key] = str(d[key])
            
    if (list_exp[1] != '0' and list_exp[1] != '1'):
        list_exp[1] = newDict[list_exp[1]]
    if (list_exp[2] != '0' and list_exp[2] != '1'):
        list_exp[2] = newDict[list_exp[2]]
    
    if (list_exp[0] == '&'): 
        result = list_exp[1] == list_exp[2] and list_exp[1] == '1'
    elif (list_exp[0] == '=>'):
        result = list_exp[1] != '1' or list_exp[2] != '0'
    elif (list_exp[0] == '|'):
        result = (list_exp[1] == '1' or list_exp[2] == '1')
    else:
        result = list_exp[1] == list_exp[2]
    
    if (result):
        return 1
    else:
        return 0

# Example test cases 
res_be1 = evaluate_with_bindings(be1,d)
res_be2 = evaluate_with_bindings(be2,d)
res_be3 = evaluate_with_bindings(be3,d)

print(f'{be1} = {res_be1}')
print(f'{be2} = {res_be2}')
print(f'{be3} = {res_be3}')


# Add the code for this function as described in the notebook 
# You can add helper functions if you want as long as the function works as expected 

def recursive_eval(l, varDict):
    newDict = {}
    a0 = '0'
    a1 = '1'
    
    for key in varDict:
        if (varDict[key] == 0 and key[:1] != '~'):
            newDict['~' + key] = '1'
        elif (varDict[key] == 1 and key[:1] != '~'):
            newDict['~' + key] = '0'
        elif (varDict[key] == 0 and key[:1] == '~'):
            newDict[key[1:]] = '1'
        elif (varDict[key] == 1 and key[:1] == '~'):
            newDict[key[1:]] = '0'
        newDict[key] = str(varDict[key])
    
    head, tail = l[0], l[1:]
    
    if head in ['~']:
        head, tail = l[1], l[2:]
        a0 = '1'
        a1 = '0'
    
    if head in ['&', '|', '=>', '<=>']: 
        val1, tail = recursive_eval(tail, newDict)
        val2, tail = recursive_eval(tail, newDict)
        
        if (val1 != '0' and val1 != '1'):
            val1 = newDict[val1]
        if (val2 != '0' and val2 != '1'):
            val2 = newDict[val2]
            
        if (head == '&'): 
            if (val1 == val2 and val1 == '1'):
                return(a1, tail)
            else:
                return(a0, tail)
        elif (head == '|'):  
            if (val1 == '1' or val2 == '1'):
                return(a1, tail)
            else:
                return(a0, tail)
        elif (head == '=>'):
            if (val1 != '1' or val2 != '0'):
                return(a1, tail)
            else:
                return(a0, tail)
        elif (head == '<=>'):
            if (val1 == val2):
                return(a1, tail)
            else:
                return(a0, tail)
    # operator is a number 
    else:  
        if (head in newDict and a0 == '1'):
            if (newDict[head] == '0'):
                return (a0, tail)
            else:
                return (a1, tail)
        elif (head in newDict):
            if (newDict[head] == '0'):
                return (a0, tail)
            else:
                return (a1, tail)
        elif (a0 == '1'):
            print('here')
            if (head == '0'):
                return (a0, tail)
            else:
                return (a1, tail)
        return (head,tail)


def prefix_eval(input_str, d): 
    input_list = input_str.split(' ')
    res, tail = recursive_eval(input_list, d)
    return int(res)

d = {"a": 1, "b": 0}
pe1 = "& a | 0 1"
pe2 = "& 0 | 1 b"
pe2 = "| 1 => ~b b"
pe3 = "<=> b <=> ~b 0"
pe4 = "=> 1 & a 0"
pe5 = "& ~a <=> 0 0"

print(d)
for e in [pe1,pe2,pe3,pe4,pe5]:
    print("%s \t = %d" % (e, prefix_eval(e,d)))

### SAMPLE OUTPUT 
# | 0 1 = 1
# <=> 1 1 = 1
# & 0 0 = 0
# {'foo': 0, 'b': 1}
# & 0 1 = 0
# & foo 1 = 0
# & foo ~b = 0
# {'a': 1, 'b': 0}
# & a | 0 1        = 1
# | 1 => ~b b      = 1
# <=> b <=> ~b 0   = 1
# => 1 & a 0       = 0
# & ~a <=> 0 0     = 0



