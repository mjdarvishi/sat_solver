# hueristic VSIDS
class  VSIDS:
    counter = {}
    def __init__(self,clauses,num_var):
        for x in range(-num_var,num_var+1):
            self.counter[x]=0
        for clause in clauses:
            for literal in clause:
                self.counter[literal] += 1

    def conflict(self,conflictClause,num_var):
        for literal in conflictClause:
            self.counter[literal]+=1
        for i in range(-num_var,num_var+1):
            self.counter[i]=self.counter[i]*95/100

    def choose(self,M,num_var):
        max=0
        var=0
        for x in range(-num_var,num_var+1):
            if self.counter[x]>=max and x not in M and -x not in M:
                    max=self.counter[x]
                    var=x
        return var