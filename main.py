from flask import Flask, render_template, request
import os
from utils.file_utility import read_cnf_file
from solvers.advance_solver import cdcl_sat_solver
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
    clouses=read_cnf_file('public/'+file.filename)
    satisfiable, model, proof=cdcl_sat_solver(clouses)
    print(satisfiable, model, proof)
    return satisfiable

@app.route('/upload-text', methods=['POST'])
def upload_text():
    # Handle text upload logic here
    text = request.form['text']
    # Process the text as needed
    return f"Text uploaded successfully: {text}"
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
