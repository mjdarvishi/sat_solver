import random
from solver.vsids import VSIDS
from solver.propagation import Propagation


class CDCL_SAT_SOLVER:
    def create_watchList(self,clauses,M,num_var):          # Create the 2-literal watch data structure
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


    def RandomRestart(self,M,back,decide_pos,probability,Restart_count):  
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




    def Analyze_Conflict(self,M, conflict,decide_pos):  #for simplicity : ALL DECISIONs made till now are a Learned Clause 
        learn = []
        for x in decide_pos:
            learn.append(-M[x])
        return learn


    def assign(self,variable,M,decide_pos):             # Adds the decision literal to M and correponding update to decision level
        decide_pos.append(len(M))
        M.append(variable)


    def add_learned_clause_to(self,clauses,literal_watch,clauses_literal_watched,Learned_c,M):
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


    def Backjump(self,M, dec_level, decide_pos,Imp_count):         #BackJump to decision level by deleting decisions from M and decision positions
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

    def solve(self,clauses,num_var):
        decide_pos = []                             # for Maintaing Decision Level
        M = []   
        propagation=Propagation()                                   # Current Assignments and implications
        clauses,M = propagation.unit(clauses)                        # Initial Unit Propogation : if conflict - UNSAT
        if clauses == -1 :
            return -1,0,0,0,0                                        # UNSAT
        back=M[:]   
        vsids=VSIDS(clauses,num_var)                                                 # Keep Initialization Backup for RESTART
        # Initialize TWO LITERAL WATCH data Structure :
        literal_watch,clauses_literal_watched = self.create_watchList(clauses,M,num_var)

        probability=0.9                                             # Random Restart Probability ,  Decays with restarts
        Restart_count = Learned_count = Decide_count = Imp_count = 0
        
        while not  len(M) >= num_var:             # While variables remain to assign
            variable = vsids.choose(M,num_var)                      # Decide : Pick a variable
            Decide_count += 1
            self.assign(variable,M,decide_pos)
            conflict,literal_watch = propagation.two_watch(clauses,literal_watch,clauses_literal_watched,M,variable)         # Deduce by Unit Propogation
            
            while conflict != -1 :
                vsids.conflict(conflict,num_var)                    # Incerements counter of literalts in conflict

                Learned_c = self.Analyze_Conflict(M, conflict,decide_pos)      #Diagnose Conflict

                dec_level = self.add_learned_clause_to(clauses,literal_watch,clauses_literal_watched,Learned_c,M) #add Learned clause to all data structures
                Learned_count += 1
                jump_status,var,Imp_count = self.Backjump(M, dec_level, decide_pos,Imp_count)      #BackJump to decision level

                if jump_status == -1:                                     # UNSAT
                    return -1,Restart_count,Learned_count,Decide_count,Imp_count
                M.append(var)                                             # Append negation of last literal after backjump
                
                probability,Restart_count = self.RandomRestart(M,back,decide_pos,probability,Restart_count)        #Random Restart
                conflict,literal_watch = propagation.two_watch(clauses,literal_watch,clauses_literal_watched,M,var)

                
        #Reaches here if all variables assigned. 

        return M,Restart_count,Learned_count,Decide_count,Imp_count
        

