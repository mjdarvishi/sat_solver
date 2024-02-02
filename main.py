from flask import Flask, render_template, request
import os
from utils.file_utility import read_cnf_file,read_cnf_text,read_file
from solver.cdcl_solver import CDCL_SAT_SOLVER
import time
app = Flask(__name__)
@app.route('/')
def home():
    file_names = os.listdir('public')
    return render_template('index.html',file_names=file_names)

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
    start_time = time.time()
    num_var,num_claus,clauses=read_cnf_file('public/'+file.filename)
    sat_solver = CDCL_SAT_SOLVER()
    solution = sat_solver.solve(clauses, num_var)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if solution[0] != -1:
        print("Assignment verified")
        assn = solution[0][:]
        assn.sort(key=abs)
        return render_template('result.html',result="\n".join(str(lit) for lit in assn),num_var=num_var,num_claus=num_claus,time=elapsed_time,clauses=solution)
    else:
        return render_template('result.html',num_var=num_var,num_claus=num_claus,clauses=solution,time=elapsed_time)
        
@app.route('/solve', methods=['POST'])
def salve():
    file = request.form['file']
    start_time = time.time()
    num_var,num_claus,clauses=read_cnf_file('public/'+file)
    sat_solver = CDCL_SAT_SOLVER()
    solution = sat_solver.solve(clauses, num_var)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if solution[0] != -1:   
        print("Assignment verified")
        assn = solution[0][:]
        assn.sort(key=abs)
        return render_template('result.html',result="\n".join(str(lit) for lit in assn),num_var=num_var,num_claus=num_claus,time=elapsed_time,clauses=solution)
    else:
        return render_template('result.html',num_var=num_var,num_claus=num_claus,clauses=solution,time=elapsed_time)
        

@app.route('/upload-text', methods=['POST'])
def upload_text():
    if request.method == 'POST':
        # Text input logic
        cnf_text = request.form['text']
        start_time = time.time()
        num_var, num_claus, clauses = read_cnf_text(cnf_text)
        # Rest of your code (as you provided)
        sat_solver = CDCL_SAT_SOLVER()
        solution = sat_solver.solve(clauses, num_var)
        end_time = time.time()
        elapsed_time = end_time - start_time
        if solution[0] != -1:
            print("Assignment verified")
            assn = solution[0][:]
            assn.sort(key=abs)
            return render_template('result.html',result="\n".join(str(lit) for lit in assn),num_var=num_var,num_claus=num_claus,time=elapsed_time,clauses=solution)
        else:
            return render_template('result.html',num_var=num_var,num_claus=num_claus,clauses=solution,time=elapsed_time)
    return 'not valid input'

@app.route('/show-problem/<name>')
def read(name):
    file_path = 'public/' + name
    content = read_file(file_path)
    return render_template('show_problem.html', content=content)
if __name__ == '__main__':
    app.run(debug=True,port=5002,host='0.0.0.0')
