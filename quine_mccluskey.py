# Quine McCluskey algorithm for minimizing logical expressions with 2-6 variables
# Author: Roxana Haghgoo

import itertools

print('\n--------------------------------------------------------------------')
print("* Minimizing Logical Expressions with 'Quine McCluskey' Algorithm * \n")

# get the number of function's variables from user
def get_functions_variables():
    run = True
    while run:
        variables = str(input('>>> Please enter the number of variables(2-6): '))
        try:
            variables = int(variables)
            if variables >= 2 and variables <= 6:
                run = False
            else:  
                print("\n> please type a number in range! \n")  
        except:   
            print("\n> please type a number! \n") 
    return variables

# get minterms and dont cares from user
variable_num = get_functions_variables()
max_range = 2 ** variable_num
run = True
while run:
    minterms = [x for x in input('>>> Please enter minterms(space between):').split()]
    d_care = [x for x in input(">>> Please enter dont cares(if any):").split()]
    md = minterms + d_care
    try:
        for i in md:
            num = int(i)
        md = list(map(int,md))
        minterms = list(map(int,minterms))
        md.sort()
        if all(num >= 0 and num < max_range for num in md):
            run = False
                
        else:
            raise ValueError
    except:
        print("\n> Something went wrong, Please try again! \n")


# convert numbers to binary form
def to_binary(num):
    binary_form = format(num, f'#0{variable_num + 2}b')
    return binary_form[2:]


# step1 = form the data --> [(minterms and dont cares number ) , ' their binary form' , checked or unched]
step1 = [[[x], str(to_binary(x)), 0] for x in md]


# Function for checking if 2 number differ by 1 bit only and putting '_' instead of difference
def find_diffrence(list1, list2):
    for a, b in itertools.combinations(list1, 2):
        only1 = 0
        res = ''
        for i in range(variable_num):
            if a[1][i] != b[1][i]:
                only1 += 1
                res += '_'
            else:
                res += a[1][i]
        if only1 == 1:
            a[2] = 1
            b[2] = 1
            list2.append([list(a[0]+b[0]), res, 0])

# step 2 = Compare step1 items with the above function and append changes  
step2 = []
find_diffrence(step1, step2)

# step 3 = compare steps2 items again to find diffrence and append changes
step3 = []
find_diffrence(step2, step3)

# find same items and remove them
for a, b in itertools.combinations(step3, 2):
    if a[1] == b[1]:
        step3.remove(b)

# find unchecked items (prime implicants)
unchecked = []
for i in step1 + step2 + step3:
    if i[2] == 0:
        unchecked.append(i)

# remove dont cares
for i in unchecked:
    i[0] = [x for x in i[0] if x in minterms]

# make a dictionary to store prime implicants data --> {'binary form' : [minterm number]}
pi_dic = {}
for i in unchecked:
    pi_dic[i[1]] = i[0]
lists = list(pi_dic.values())

# function to find essencial prime implicants
def essencial_pi(indexes=None, s=None, index=None):
    if indexes is None:
        indexes = []
    if s is None:
        s = set()
    if index is None:
        index = 0
    if s >= set(minterms):
        return indexes
    if index >= len(lists):
        return False
    s1 = essencial_pi(indexes + [index], s | set(lists[index]), index + 1)
    s2 = essencial_pi(indexes, s, index + 1)
    if not s1 and not s2:
        return False
    if not s1:
        return s2
    if not s2:
        return s1
    if len(s1) < len(s2):
        return s1
    return s2

# essencial prime implicants
epi = essencial_pi()

# Function to find variables algabric form. For example, the minterm 1--0 is AD' 
def to_Algebraic(string):
    replace = ""
    index = 1
    for i in string:
        if i == '1':
            char = str(chr(index+64))
            replace += char
            index += 1
        elif i == '0':
            char = str(chr(index+64)) + "'"
            replace += char
            index += 1
        else:
            index += 1
            continue
    return replace

# display result
result = ''
keys = list(pi_dic.keys())
for j in epi:
    result += str(to_Algebraic(keys[j])) + ' + '

function_variable =','.join([chr(i+65) for i in range(variable_num)])
print(f'\n>>> f({function_variable}) = {result[:-2]}\n')
print('--------------------------------------------------------------------')


