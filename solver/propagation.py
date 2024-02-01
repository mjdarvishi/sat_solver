class Propagation:
    def unit(self,clauses):             
        assignment = []
        flag=1
        while flag!=0:                      
            flag=0
            for x in clauses:              
                if len(x) == 1 :               
                    unit=x[0]
                    clauses = self.__bcp(clauses, unit) 
                    assignment += [unit]
                    flag=1
                if clauses == -1:                
                    return -1, []
                if not clauses:                   
                    return clauses, assignment
        return clauses, assignment

    def two_watch(self,clauses,literal_watch,clauses_literal_watched,M,variable): 
        prop_list = [variable]            
        while len(prop_list) != 0 :        
            variable = prop_list.pop()     
            for affected_claus_num in reversed(literal_watch[-variable]) : 
                affected_claus = clauses[affected_claus_num][:]
                A = clauses_literal_watched[affected_claus_num][0]
                B = clauses_literal_watched[affected_claus_num][1]
                A_prev=A
                B_prev=B
                status,M,A,B,unit = self.__check_status(affected_claus,M,A,B)    
                if status == "Unit" :
                    prop_list.append(unit)
                    M.append(unit)                                       
                elif status == "Unsatisfied":                            
                    return affected_claus,literal_watch
                                                                        
                literal_watch [A_prev].remove(affected_claus_num)
                literal_watch [B_prev].remove(affected_claus_num)
                clauses_literal_watched[affected_claus_num][0] = A
                clauses_literal_watched[affected_claus_num][1] = B
                literal_watch [A].append(affected_claus_num)
                literal_watch [B].append(affected_claus_num)
                
        return -1,literal_watch

    def __check_status(self,clause,M,A,B):
        unit = 0
        if A in M or B in M:                  
            return "Satisied",M,A,B,unit
        sym=[]                                 
        for literal in clause:                 
            if -literal not in M:
                sym.append(literal)
            if literal in M :
                if -A not in M :
                    return "Satisied",M,A,literal,unit
                return "Satisied",M,literal,B,unit
        if len(sym) == 1:                             
            return "Unit",M,A,B,sym[0]
        if len(sym) == 0:                             
            return "Unsatisfied",M,A,B,unit
        else :
            return "Unresolved",M,sym[0],sym[1],unit  
        
    def __bcp(self,clauses, literal):                   
        new_claus_set = [x[:] for x in clauses]  
        for x in reversed(new_claus_set):
            if literal in x:                      
                new_claus_set.remove(x)             
            if -literal in x:                   
                x.remove(-literal)                   
                if not x:                       
                    return -1
        return new_claus_set



