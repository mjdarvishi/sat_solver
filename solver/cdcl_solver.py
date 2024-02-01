import random
from solver.vsids import VSIDS
from solver.propagation import Propagation
from solver.proof_generator import ProofGenerator

class CDCL_SAT_SOLVER:
    def __init__(self):
        self.proof_generator = ProofGenerator()
     # Create the 2-literal watch data structure
    def watchList_creation(self,clauses,M,num_var):         
        literal_watch = {}                  
        clauses_literal_watched = []        
        for i in range (-num_var,num_var+1):
            literal_watch[i] = []
        for i in range (0,len(clauses)):   
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
            clauses_literal_watched.append(newc)      
            literal_watch[A].append(i)                
            literal_watch[B].append(i)
        return literal_watch,clauses_literal_watched


    def restart_randomly(self,M,back,decide_pos,probability,Restart_count):  
        if random.random() < probability :          
            M = back[:]
            decide_pos = []
            probability *= 0.5                     
            Restart_count += 1
            if probability < 0.001 :
                probability = 0.2
            if Restart_count > len(M) + 10:        
                probability=0
        return probability,Restart_count




    def conf_analize(self,M, conflict,decide_pos):  
        learn = []
        for x in decide_pos:
            learn.append(-M[x])
        return learn


    def assign(self,variable,M,decide_pos):             
        decide_pos.append(len(M))
        M.append(variable)


    def add_learned_clause_to(self,clauses,literal_watch,clauses_literal_watched,Learned_c,M):
        if len(Learned_c) == 0:
            return -1
        if len(Learned_c) == 1:            
            M.append(Learned_c[0])
            return 1,Learned_c[0]
        clauses.append(Learned_c)          
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


    def Backjump(self,M, dec_level, decide_pos,Imp_count):        
        Imp_count = Imp_count + len(M) - len(decide_pos)
        if not decide_pos:
            return -1,-1,Imp_count
        dec_level = decide_pos.pop()
        literal = M[dec_level]
        del M[dec_level:]
        return 0,-literal,Imp_count

    def solve(self,clauses,num_var):
        decide_pos = []                       
        M = []   
        propagation=Propagation()                              
        clauses,M = propagation.unit(clauses)                    
        if clauses == -1 :
            return -1,0,0,0,0                                     
        back=M[:]   
        vsids=VSIDS(clauses,num_var)                                           
        literal_watch,clauses_literal_watched = self.watchList_creation(clauses,M,num_var)

        probability=0.9                                         
        Restart_count = Learned_count = Decide_count = Imp_count = 0
        
        while not  len(M) >= num_var:         
            variable = vsids.choose(M,num_var)     
            Decide_count += 1
            self.assign(variable,M,decide_pos)
            conflict,literal_watch = propagation.two_watch(clauses,literal_watch,clauses_literal_watched,M,variable) 
            
            while conflict != -1 :
                vsids.conflict(conflict,num_var)                

                Learned_c = self.conf_analize(M, conflict,decide_pos)    

                dec_level = self.add_learned_clause_to(clauses,literal_watch,clauses_literal_watched,Learned_c,M) 
                Learned_count += 1
                jump_status,var,Imp_count = self.Backjump(M, dec_level, decide_pos,Imp_count)  

                if jump_status == -1:                               
                    return -1,Restart_count,Learned_count,Decide_count,Imp_count,self.proof_generator.proof_steps 
                M.append(var)                                    
                
                probability,Restart_count = self.restart_randomly(M,back,decide_pos,probability,Restart_count)      
                conflict,literal_watch = propagation.two_watch(clauses,literal_watch,clauses_literal_watched,M,var)
                #Proof
                if  len(self.proof_generator.proof_steps)<500:
                    if isinstance(dec_level, tuple):
                        # Choose one of the tuple elements or convert the tuple to a single value based on your logic
                        dec_level = dec_level[0]
                    self.proof_generator.add_proof_step(clauses_literal_watched[dec_level][0], clauses_literal_watched[dec_level][1],Learned_c) 
        return M,Restart_count,Learned_count,Decide_count,Imp_count,self.proof_generator.proof_steps
        

