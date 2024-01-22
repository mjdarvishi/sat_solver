# hueristic VSIDS
class  VSIDS:
    counter = {}
    # init counter and count appearance of each literal 
    def __init__(self,clauses,num_var):
        for x in range(-num_var,num_var+1):
            self.counter[x]=0
        for clause in clauses:
            for literal in clause:
                self.counter[literal] += 1

    # incerement counter of literalt in conflict
    def conflict(self,conflictClause,num_var):
        for literal in conflictClause:
            self.counter[literal]+=1
        # Counter is reduced by 5% for all literals at each conflict
        for i in range(-num_var,num_var+1):
            self.counter[i]=self.counter[i]*95/100

    # Picks a Variable NOT yet in M based on max counter value
    def choose(self,M,num_var):
        max=0
        var=0
        for x in range(-num_var,num_var+1):
            if self.counter[x]>=max and x not in M and -x not in M:
                    max=self.counter[x]
                    var=x
        return var