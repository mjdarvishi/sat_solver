from solvers.advance_solver import sat_solver_with_advanced_features



# Get CNF clauses from the user
print("Enter CNF clauses, one clause per line. Enter an empty line to finish.")
cnf_input = []
while True:
    clause_input = input("Clause: ")
    if not clause_input:
        break
    cnf_input.append(list(map(int, clause_input.split())))

# Call the solver function
sat_solver_with_advanced_features(cnf_input)
