# Following functions are for hueristic VSIDS

# Initiatilaztion  : Generated counter for number of times a literal appears
def VSIDS_init(clauses,num_var):
    counter = {}
    for x in range(-num_var,num_var+1):
        counter[x]=0
    for clause in clauses:
        for literal in clause:
            counter[literal] += 1
    return counter

# conflict : Incerements counter of literalts in conflict clause to increase there chances of getting selected
def VSIDS_conflict(counter,conflictClause):
    for literal in conflictClause:
        counter[literal]+=1
    return counter

# decay : Counter is reduced by 5% for all literals at each conflict
def VSIDS_decay(counter,num_var):
    for i in range(-num_var,num_var+1):
        counter[i]=counter[i]*95/100
    return counter

# decide : Picks a Variable NOT yet in M based on max counter value
def VSIDS_decide(counter,M,num_var):
    max=0
    var=0
    for x in range(-num_var,num_var+1):
        if counter[x]>=max and x not in M and -x not in M:
                max=counter[x]
                var=x
    return var