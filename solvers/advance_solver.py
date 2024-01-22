from pysat.solvers import Glucose3

def cdcl_sat_solver(cnf_clauses):
    # Create a solver instance with proof generation enabled
    solver = Glucose3(bootstrap_with=[], with_proof=True)

    # Assign initial scores to variables
    variable_scores = {}

    # Maintain a list of clauses for proof generation
    proof_clauses = []

    # Add clauses with two watched literals and update variable scores
    for clause in cnf_clauses:
        if len(clause) > 0:
            watch_literals(clause, solver, variable_scores, proof_clauses)

    # Assume all variables are initially undecided (unassigned)
    decisions = []
    model = None
    satisfiable = False
    while True:
        # Choose a variable to make a decision based on the VSIDS heuristic
        decision_variable = choose_variable(variable_scores)
        # If there are no more decisions, the problem is solved
        if decision_variable is None:
            model = solver.get_model()
            satisfiable = True
            break

        # Make the decision
        decisions.append(decision_variable)
        solver.add_clause([decision_variable])

        # Solve with current assumptions
        is_satisfiable = solver.solve(assumptions=decisions)

        # If the problem is satisfiable, get the model
        if is_satisfiable:
            model = solver.get_model()
            satisfiable = True
            break
        else:
            # Analyze conflict and backtrack using First-UIP heuristic
            learned_clause = analyze_conflict(proof_clauses[-1], solver)
            if not learned_clause:
                satisfiable = False
                break

            # Add the learned clause to the solver and update variable scores
            watch_literals(learned_clause, solver, variable_scores, proof_clauses)
            solver.add_clause(learned_clause)

            # Backtrack to the specified decision level
            decisions = backtrack(decisions, learned_clause)

    # Generate a proof based on the stored clauses
    proof = generate_proof(proof_clauses, solver)
    print("Proof:", proof)
    return satisfiable, model, proof

def watch_literals(clause, solver, variable_scores, proof_clauses):
    # Add a clause with two watched literals to the solver
    if len(clause) == 0:
        raise ValueError("Clause must not be empty")
    elif len(clause) == 1:
        solver.add_clause(clause)
    else:
        # Update variable scores based on the watched literals
        for lit in clause:
            var = abs(lit)
            variable_scores[var] = variable_scores.get(var, 0) + 1
        solver.add_clause([clause[0], clause[1]])

        # Store the clause for proof generation
        proof_clauses.append(clause)

def choose_variable(variable_scores):
    # Choose a variable based on the VSIDS heuristic
    max_score = 0
    chosen_variable = None
    for var, score in variable_scores.items():
        if score > max_score:
            max_score = score
            chosen_variable = var
    return chosen_variable

def analyze_conflict(conflict_clause, solver):
    # The learned clause is the conflict clause without the UIP literal
    learned_clause = [lit for lit in conflict_clause]

    return learned_clause

def backtrack(decisions, learned_clause):
    # Backtrack to the specified decision level
    backtrack_level = len(decisions)

    for lit in learned_clause:
        var = abs(lit)
        if var in decisions:
            backtrack_level = min(backtrack_level, decisions.index(var) + 1)
    return decisions[:backtrack_level]



def generate_proof(clauses, solver):
    proof_clauses = []
    for conflict in clauses:
        # Analyze the conflict and extract the learned clause
        learned_clause = analyze_conflict(conflict, solver)
        if not learned_clause:
            # If no learned clause, stop generating the proof
            break

        # Add the learned clause to the proof clauses
        proof_clauses.extend(learned_clause)

    # Return the proof as a list of clauses
    return proof_clauses
