import re
import re

def has_logical_operators(line):
    return any(op in line for op in ['AND', 'OR'])

def convert_to_cnf_from_custom_format(input_string):
    input_string = input_string.replace('AND', ' & ').replace('OR', ' | ').replace('NOT', ' ~')

    input_string = input_string.replace('(', '').replace(')', '')

    clauses = input_string.split('AND')

    cnf_clauses = []
    for clause in clauses:
        literals = clause.strip().split('OR')
        cnf_clause = []
        for literal in literals:
            cnf_clause.append(literal.strip())
        cnf_clauses.append(cnf_clause)

    return cnf_clauses


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

def read_file(file_path):
    f = open(file_path, "r")
    return f.read()

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