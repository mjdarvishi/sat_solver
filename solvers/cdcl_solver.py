import random
from solvers.vsids import VSIDS

def bcp(clauses, literal):                    #Boolean Constant Propagation on Literal
    new_claus_set = [x[:] for x in clauses]   #Using SLicing Technique: Fastest available in Python
    for x in reversed(new_claus_set):
        if literal in x:                      #if clause satified ,
            new_claus_set.remove(x)                    #Remove that clause
        if -literal in x:                     #if -literal present , remaining should satisfy . Hence,
            x.remove(-literal)                         #Remove -literal from that clause
            if not x:                         #if this makes a clause Empty , UNSAT
                return -1
    return new_claus_set

def unit_propagation(clauses):               # Propogate Unit Clauses and add implications to M
    assignment = []
    flag=1
    while flag!=0:                           #till Implications are found
        flag=0
        for x in clauses:                    #for each clause
            if len(x) == 1 :                 # if UNIT clause , propagate and add to assignment
                unit=x[0]
                clauses = bcp(clauses, unit) 
                assignment += [unit]
                flag=1
            if clauses == -1:                #if UNSAT after propogate, return -1
                return -1, []
            if not clauses:                   
                return clauses, assignment
    return clauses, assignment

def create_watchList(clauses,M,num_var):          # Create the 2-literal watch data structure
    literal_watch = {}                    # Will contain the main Literal-> Clause number mapping
    clauses_literal_watched = []          # The reverse,i.e. Clause-> Literal mapping
    for i in range (-num_var,num_var+1):
        literal_watch[i] = []
    for i in range (0,len(clauses)):      #for each clause pick two literals
        newc = []
        first = 0
        for j in range(0,len(clauses[i])):
            if clauses[i][j] not in M and first==0:
                A = clauses[i][j]
                first=1
                continue
            if clauses[i][j] not in M and first==1:
                B = clauses[i][j]
                break
        newc.append(A)
        newc.append(B)
        clauses_literal_watched.append(newc)       #add both to watched of that clause 
        literal_watch[A].append(i)                 #add clause to watch of those literals
        literal_watch[B].append(i)
    return literal_watch,clauses_literal_watched

# Function to propogate using 2-literal watch

def two_watch_propogate(clauses,literal_watch,clauses_literal_watched,M,variable): 
    prop_list = [variable]             # add current change to list of updates
    while len(prop_list) != 0 :        # while updates remain to propogate
        variable = prop_list.pop()     #pick one variable
        for affected_claus_num in reversed(literal_watch[-variable]) : #for all clauses in its watch list
            affected_claus = clauses[affected_claus_num][:]
            A = clauses_literal_watched[affected_claus_num][0]
            B = clauses_literal_watched[affected_claus_num][1]
            A_prev=A
            B_prev=B
            status,M,A,B,unit = check_status(affected_claus,M,A,B)     # check status of each clause
            if status == "Unit" :
                prop_list.append(unit)
                M.append(unit)                                         # if unit, add to updates
            elif status == "Unsatisfied":                              #if unsat, return conflict clause
                return affected_claus,literal_watch
                                                                       #else the clause is still unresolve, remove from current add to proper watch
            literal_watch [A_prev].remove(affected_claus_num)
            literal_watch [B_prev].remove(affected_claus_num)
            clauses_literal_watched[affected_claus_num][0] = A
            clauses_literal_watched[affected_claus_num][1] = B
            literal_watch [A].append(affected_claus_num)
            literal_watch [B].append(affected_claus_num)
            
    return -1,literal_watch


def check_status(clause,M,A,B):
    unit = 0
    if A in M or B in M:                   # if one watch satisfied, nothing to do 
        return "Satisied",M,A,B,unit
    sym=[]                                  # symbols not defined yet
    for literal in clause:                  # find symbols not defined
        if -literal not in M:
            sym.append(literal)
        if literal in M :
            if -A not in M :
                return "Satisied",M,A,literal,unit
            return "Satisied",M,literal,B,unit
    if len(sym) == 1:                              # if one such symbol -> Unit Clause
        return "Unit",M,A,B,sym[0]
    if len(sym) == 0:                              # if no such symbol -> Unsatisfied (conflict) clause
        return "Unsatisfied",M,A,B,unit
    else :
        return "Unresolved",M,sym[0],sym[1],unit   # else return two new unsatisfied variables to use for Literal_watch


def RandomRestart(M,back,decide_pos,probability,Restart_count):  
    if random.random() < probability :          # If Generated random probability less than current : RESTART
        M = back[:]
        decide_pos = []
        probability *= 0.5                      # Decay next Restart probability by 50%
        Restart_count += 1
        if probability < 0.001 :
            probability = 0.2
        if Restart_count > len(M) + 10:         #avoid restarts if already restarted many times
            probability=0
    return probability,Restart_count


def verify(M,clauses) :                  # Verify the Solution in M for SAT
    for c in clauses :                   # for each clause
        flag = 0
        for lit in c:
            if lit in M:                 # atleast one literal should be true
                flag = 1
                break
        if flag == 0:
            return False
    return True


def Analyze_Conflict(M, conflict,decide_pos):  #for simplicity : ALL DECISIONs made till now are a Learned Clause 
    learn = []
    for x in decide_pos:
        learn.append(-M[x])
    return learn


def all_vars_assigned(num_var ,M_len):        # Returns True if all variables already assigne , False otherwise
    if M_len >= num_var:
        return True
    return False


def assign(variable,M,decide_pos):             # Adds the decision literal to M and correponding update to decision level
    decide_pos.append(len(M))
    M.append(variable)


def add_learned_clause_to(clauses,literal_watch,clauses_literal_watched,Learned_c,M):
    if len(Learned_c) == 0:
        return -1
    if len(Learned_c) == 1:             # if unit clause is learnt : add it as a decision 
        M.append(Learned_c[0])
        return 1,Learned_c[0]
    clauses.append(Learned_c)           # for others, add two literals A,B to literal watch data structure
    A = Learned_c[0]
    B = Learned_c[1]
    i = len(clauses)-1
    newc = []
    newc.append(A)
    newc.append(B)
    clauses_literal_watched.append(newc)
    literal_watch[A].append(i)
    literal_watch[B].append(i)
    return 0


def Backjump(M, dec_level, decide_pos,Imp_count):         #BackJump to decision level by deleting decisions from M and decision positions
    Imp_count = Imp_count + len(M) - len(decide_pos)
    if not decide_pos:
        return -1,-1,Imp_count
    dec_level = decide_pos.pop()
    literal = M[dec_level]
    del M[dec_level:]
    return 0,-literal,Imp_count

# def progressBar(current, total, barLength = 20) :        # Print progress bar. Just to givee feel of work being done
#     percent = float(current) * 100 / total
#     arrow   = '-' * int(percent/100 * barLength - 1) + '>'
#     spaces  = ' ' * (barLength - len(arrow))
#     print('Progress (num_var:may backtrack): [%s%s] %d ' % (arrow, spaces, current), end='\r')

def CDCL_solve(clauses,num_var):
    decide_pos = []                             # for Maintaing Decision Level
    M = []                                      # Current Assignments and implications
    clauses,M = unit_propagation(clauses)                        # Initial Unit Propogation : if conflict - UNSAT
    if clauses == -1 :
        return -1,0,0,0,0                                        # UNSAT
    back=M[:]   
    vsids=VSIDS(clauses,num_var)                                                 # Keep Initialization Backup for RESTART
    # Initialize TWO LITERAL WATCH data Structure :
    literal_watch,clauses_literal_watched = create_watchList(clauses,M,num_var)

    probability=0.9                                             # Random Restart Probability ,  Decays with restarts
    Restart_count = Learned_count = Decide_count = Imp_count = 0
    
    while not all_vars_assigned(num_var , len(M)) :             # While variables remain to assign
        variable = vsids.VSIDS_decide(M,num_var)                      # Decide : Pick a variable
        Decide_count += 1
        assign(variable,M,decide_pos)
        conflict,literal_watch = two_watch_propogate(clauses,literal_watch,clauses_literal_watched,M,variable)         # Deduce by Unit Propogation
        
        while conflict != -1 :
            vsids.VSIDS_conflict(conflict)                    # Incerements counter of literalts in conflict
            vsids.VSIDS_decay(num_var)                # Decay counters by 5%

            Learned_c = Analyze_Conflict(M, conflict,decide_pos)      #Diagnose Conflict

            dec_level = add_learned_clause_to(clauses,literal_watch,clauses_literal_watched,Learned_c,M) #add Learned clause to all data structures
            Learned_count += 1
            jump_status,var,Imp_count = Backjump(M, dec_level, decide_pos,Imp_count)      #BackJump to decision level

            if jump_status == -1:                                     # UNSAT
                return -1,Restart_count,Learned_count,Decide_count,Imp_count
            M.append(var)                                             # Append negation of last literal after backjump
            
            probability,Restart_count = RandomRestart(M,back,decide_pos,probability,Restart_count)        #Random Restart
            conflict,literal_watch = two_watch_propogate(clauses,literal_watch,clauses_literal_watched,M,var)

            
    #Reaches here if all variables assigned. 

    return M,Restart_count,Learned_count,Decide_count,Imp_count
    

