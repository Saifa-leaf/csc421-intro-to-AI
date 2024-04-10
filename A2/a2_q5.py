
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
#             print(newDict)
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

def prefix_eval(input_str, varDict): 
    input_list = input_str.split(' ')
    res, tail = recursive_eval(input_list, varDict)
    return res

def genComb(string):
    output = []
    
    elements = string.split()
    genRecur(elements, 0, output)
    
    return output

def genRecur(elements, index, output):
    if index == len(elements):
        output.append(' '.join(elements))
        return

    if elements[index].isalpha():
        genRecur(elements, index + 1, output)
        elements[index] = '~' + elements[index]
        genRecur(elements, index + 1, output)
        elements[index] = elements[index][1:]
    elif elements[index].startswith('~'):
        genRecur(elements, index + 1, output)
        elements[index] = elements[index][1:]
        genRecur(elements, index + 1, output)
        elements[index] = '~' + elements[index]
    else:
        genRecur(elements, index + 1, output)

def entail(kb, alpha):
    diction = {}
    
    KBList = genComb(kb)
    
    letters = kb.split()
    for letter in letters:
        if letter.isalpha():
            diction[letter] = 1
        elif letter.startswith('~'):
            diction[letter] = 0
            
    for a in KBList:
        diction = {}
        letters = a.split()
        for letter in letters:
            if letter.isalpha():
                diction[letter] = 1
            elif letter.startswith('~'):
                diction[letter] = 0
        aAns = prefix_eval(a, diction)
        if (aAns == '1'):
            newDiction = {}
            for b in alpha.split():
                if (b.startswith('~') and b[1:] in diction ):
                    newDiction[b] = diction[b[1:]]
                elif ('~'+(b) in diction):
                    newDiction[b] = diction['~'+(b)]
                elif (b.isalpha()):
                    newDiction[b] = diction[b]
                    

            bAns = prefix_eval(b, newDiction)
            if (bAns == '0'):
                return False
            
    return True

KBpre = '& A & | B C & D & E & ~F ~G'
ALpre = '& A & D & E & ~F ~G'

k = '| X Y'
a = '& Y X'

print("KB: " + KBpre)
print("a: " + ALpre)
print(entail(KBpre, ALpre))
print("KB: " + k)
print("a: " + a)
print(entail(k,a))
