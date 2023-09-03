import numpy as np
import model
from flask import Flask, request, render_template
import pickle
import webbrowser

app = Flask(__name__,template_folder="templates")
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
def predict():
    
    gender = request.args.get('gender')
    ssc_p = float(request.args.get('ssc_p'))
    ssc_b = request.args.get('ssc_b')
    hsc_p = float(request.args.get('hsc_p'))
    hsc_b = request.args.get('hsc_b')
    hsc_s = request.args.get('hsc_s')
    degree_p = float(request.args.get('degree_p'))
    degree_t = request.args.get('degree_t')
    workex = request.args.get('workex')
    etest_p = float(request.args.get('etest_p'))
    specialisation = request.args.get('specialisation')
    mba_p = float(request.args.get('mba_p'))
    
    # Convert categorical variables to numeric values
    gender_num = 1 if gender == 'Male' else 0
    ssc_b_num = 1 if ssc_b == 'Central' else 0
    hsc_b_num = 1 if hsc_b == 'Central' else 0
    hsc_s_num = 0  # Default value
    if hsc_s == 'Science':
        hsc_s_num = 1
    elif hsc_s == 'Arts':
        hsc_s_num = 2
    
    degree_t_num = 0  # Default value
    if degree_t == 'Sci&Tech':
        degree_t_num = 1
    elif degree_t == 'Comm&Mgmt':
        degree_t_num = 2
    
    workex_num = 1 if workex == 'Yes' else 0
    specialisation_num = 0  # Default value
    if specialisation == 'Mkt&HR':
        specialisation_num = 1
    
    # Create an array of input values
    input_arr = [gender_num, ssc_p, ssc_b_num, hsc_p, hsc_b_num, hsc_s_num, degree_p, degree_t_num, workex_num, etest_p, specialisation_num, mba_p]
    input_arr = np.asarray(input_arr, dtype=float)
    
    output = model.predict([input_arr])
    
    if output == 1:
        out = 'You are placed'
    else:
        out = 'You might not get placed'
        
    return render_template('out.html', output=out)

if __name__ == "__main__":
    # Open the web browser automatically
    webbrowser.open('http://127.0.0.1:5000/')
    # Run the app
    app.run(debug=True)
