class Propagation:
    def unit(self,clauses):               # Propogate Unit Clauses and add implications to M
        assignment = []
        flag=1
        while flag!=0:                           #till Implications are found
            flag=0
            for x in clauses:                    #for each clause
                if len(x) == 1 :                 # if UNIT clause , propagate and add to assignment
                    unit=x[0]
                    clauses = self.__bcp(clauses, unit) 
                    assignment += [unit]
                    flag=1
                if clauses == -1:                #if UNSAT after propogate, return -1
                    return -1, []
                if not clauses:                   
                    return clauses, assignment
        return clauses, assignment

    def two_watch(self,clauses,literal_watch,clauses_literal_watched,M,variable): 
        prop_list = [variable]             # add current change to list of updates
        while len(prop_list) != 0 :        # while updates remain to propogate
            variable = prop_list.pop()     #pick one variable
            for affected_claus_num in reversed(literal_watch[-variable]) : #for all clauses in its watch list
                affected_claus = clauses[affected_claus_num][:]
                A = clauses_literal_watched[affected_claus_num][0]
                B = clauses_literal_watched[affected_claus_num][1]
                A_prev=A
                B_prev=B
                status,M,A,B,unit = self.__check_status(affected_claus,M,A,B)     # check status of each clause
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

    def __check_status(self,clause,M,A,B):
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
        
    def __bcp(self,clauses, literal):                    #Boolean Constant Propagation on Literal
        new_claus_set = [x[:] for x in clauses]   #Using SLicing Technique: Fastest available in Python
        for x in reversed(new_claus_set):
            if literal in x:                      #if clause satified ,
                new_claus_set.remove(x)                    #Remove that clause
            if -literal in x:                     #if -literal present , remaining should satisfy . Hence,
                x.remove(-literal)                         #Remove -literal from that clause
                if not x:                         #if this makes a clause Empty , UNSAT
                    return -1
        return new_claus_set



