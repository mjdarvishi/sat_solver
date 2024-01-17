def read_cnf_file(file_path):
    cnf_clauses = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue  # Skip comment and problem description lines
            clause = list(map(int, line.split()[:-1]))  # Exclude the '0' at the end
            cnf_clauses.append(clause)
    return cnf_clauses