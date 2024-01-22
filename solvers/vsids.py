# Following functions are for hueristic VSIDS

class  VSIDS:
    counter = {}
    # Generated counter for number of times a literal appears
    def __init__(self,clauses,num_var):
        for x in range(-num_var,num_var+1):
            self.counter[x]=0
        for clause in clauses:
            for literal in clause:
                self.counter[literal] += 1

    # Incerements counter of literalts in conflict clause to increase there chances of getting selected
    def VSIDS_conflict(self,conflictClause):
        for literal in conflictClause:
            self.counter[literal]+=1

    # Counter is reduced by 5% for all literals at each conflict
    def VSIDS_decay(self,num_var):
        for i in range(-num_var,num_var+1):
            self.counter[i]=self.counter[i]*95/100

    # Picks a Variable NOT yet in M based on max counter value
    def VSIDS_decide(self,M,num_var):
        max=0
        var=0
        for x in range(-num_var,num_var+1):
            if self.counter[x]>=max and x not in M and -x not in M:
                    max=self.counter[x]
                    var=x
        return var