def read_cnf_file(file_path):
    cnf_clauses = []
    num_variables = 0
    num_clauses = 0

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                if line.startswith('p'):
                    parts = line.split()
                    num_variables = int(parts[2])
                    num_clauses = int(parts[3])
                continue  # Skip comment and problem description lines
            
            clause = list(map(int, line.split()[:-1]))  # Exclude the '0' at the end
            cnf_clauses.append(clause)

    return num_variables, num_clauses, cnf_clauses

def read_cnf_text(cnf_text):
    cnf_clauses = []
    num_variables = 0
    num_clauses = 0

    # Parse CNF text
    lines = cnf_text.split('\n')
    for line in lines:
        if line.startswith('c') or line.startswith('p'):
            if line.startswith('p'):
                parts = line.split()
                num_variables = int(parts[2])
                num_clauses = int(parts[3])
            continue  # Skip comment and problem description lines

        clause = list(map(int, line.split()[:-1]))  # Exclude the '0' at the end
        cnf_clauses.append(clause)

    return num_variables, num_clauses, cnf_clauses