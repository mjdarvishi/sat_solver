from flask import Flask, render_template, request
import os
from utils.file_utility import read_cnf_file,read_cnf_text
from solver.cdcl_solver import CDCL_SAT_SOLVER

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file provided"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    # Process the file as needed
    # For example, you can save it or perform operations on its content
    file.save(os.path.join('public', file.filename))
    num_var,num_claus,clauses=read_cnf_file('public/'+file.filename)
    sat_solver = CDCL_SAT_SOLVER()  
    solution=sat_solver.solve(clauses,num_var)
    if solution[0] != -1:
        print("Assignment verified")
        assn = solution[0][:]
        assn.sort(key=abs)
        return render_template('result.html',reuslt="\n".join(str(lit) for lit in assn))
    else :
        return render_template('result.html')
        

@app.route('/upload-text', methods=['POST'])
def upload_text():
    if request.method == 'POST':
        # Text input logic
        cnf_text = request.form['text']
        num_var, num_claus, clauses = read_cnf_text(cnf_text)

        # Rest of your code (as you provided)
        sat_solver = CDCL_SAT_SOLVER()
        solution = sat_solver.solve(clauses, num_var)
        if solution[0] != -1:
            print("Assignment verified")
            assn = solution[0][:]
            assn.sort(key=abs)
            return render_template('result.html',result="\n".join(str(lit) for lit in assn))
        else:
            return render_template('result.html')
    return 'not valid input'
if __name__ == '__main__':
    app.run(debug=True)



# # Get CNF clauses from the user
# print("Enter CNF clauses, one clause per line. Enter an empty line to finish.")
# cnf_input = []
# while True:
#     clause_input = input("Clause: ")
#     if not clause_input:
#         break
#     cnf_input.append(list(map(int, clause_input.split())))

# # Call the solver function
# cdcl_sat_salver(cnf_input)
