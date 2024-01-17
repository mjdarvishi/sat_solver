from pysat.solvers import Glucose3
from pysat.formula import CNF

def sat_solver_with_advanced_features(cnf_clauses):
    cnf_formula = CNF()
    cnf_formula.clauses.extend(cnf_clauses)
    # Create a solver instance with proof generation enabled
    solver = Glucose3(bootstrap_with=[], with_proof=True)

    # Assign initial scores to variables
    variable_scores = {}

    # Maintain a list of clauses for proof generation
    proof_clauses = []

    # Add clauses with two watched literals and update variable scores
    for clause in cnf_formula.clauses:
        watch_literals(clause, solver, variable_scores)

    # Assume all variables are initially undecided (unassigned)
    decisions = []
    propagations = []
    while True:
        # PART(C)
        # Choose a variable to make a decision based on the VSIDS heuristic
        decision_variable = choose_variable(variable_scores)

        # If there are no more decisions, the problem is solved
        if decision_variable is None:
            print("Satisfiable! Model:", solver.get_model())
            break

        # Make the decision
        decisions.append(decision_variable)
        solver.add_clause([decision_variable])

        # Store the decision clause for proof generation
        proof_clauses.append([decision_variable])

        # Solve with current assumptions
        is_satisfiable = solver.solve(assumptions=decisions)

        # If the problem is satisfiable, get the model
        if is_satisfiable:
            model = solver.get_model()
            print("Satisfiable! Model:", model)
            break
        else:
            # PART(A)
            # Analyze conflict and backtrack using First-UIP heuristic
            conflict = solver.get_conflict()
            learned_clause = analyze_conflict(conflict, solver)
            if not learned_clause:
                print("Unsatisfiable")
                break

            # Add the learned clause to the solver and update variable scores
            watch_literals(learned_clause, solver, variable_scores)
            solver.add_clause(learned_clause)

            # Store the learned clause for proof generation
            proof_clauses.append(learned_clause)

            # Update decisions based on the learned clause
            backtrack_level = update_decisions(learned_clause, decisions)
            if backtrack_level == 0:
                print("Unsatisfiable")
                break

            # Backtrack to the specified decision level
            solver.cancel_until(backtrack_level)
            decisions = decisions[:backtrack_level]
            propagations = propagations[:backtrack_level]

    # Generate a proof based on the stored clauses
    proof = generate_proof(proof_clauses, solver)
    print("Proof:", proof)

def watch_literals(clause, solver, variable_scores):
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

def choose_variable(variable_scores):
    # Choose a variable based on the VSIDS heuristic
    max_score = 0
    chosen_variable = None
    for var, score in variable_scores.items():
        if score > max_score:
            max_score = score
            chosen_variable = var
    return chosen_variable

def update_decisions(learned_clause, decisions):
    # Update decisions based on the learned clause and backtrack level
    # This is a simplified example, and a full update requires more complex logic
    backtrack_level = 0
    for lit in learned_clause:
        var = abs(lit)
        if var in decisions:
            backtrack_level = max(backtrack_level, decisions.index(var) + 1)
    return backtrack_level

def analyze_conflict(conflict, solver):
    # Sort the literals in the conflict clause by their decision levels
    sorted_literals = sorted(conflict, key=lambda lit: solver.level(abs(lit)), reverse=True)

    # Identify the UIP literal (the first literal with a unique decision level)
    unique_levels = set()
    uip_literal = None

    for lit in sorted_literals:
        level = solver.level(abs(lit))

        if level not in unique_levels:
            unique_levels.add(level)
            uip_literal = lit

    # The learned clause is the conflict clause without the UIP literal
    learned_clause = [lit for lit in conflict if lit != -uip_literal]

    return learned_clause

def generate_proof(clauses, solver):
    proof_clauses = []
    for conflict in clauses:
        # Analyze the conflict and extract the learned clause
        learned_clause = analyze_conflict(conflict, solver)
        if not learned_clause:
            # If no learned clause, stop generating the proof
            break

        # Add the learned clause to the proof clauses
        proof_clauses.append(learned_clause)

        # Update decisions based on the learned clause
        backtrack_level = update_decisions(learned_clause, decisions)

        # Backtrack to the specified decision level
        decisions = decisions[:backtrack_level]

    # Return the proof as a list of clauses
    return proof_clauses

