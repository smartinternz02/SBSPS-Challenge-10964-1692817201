import numpy as np
from flask import Flask, request, render_template
app = Flask(__name__,template_folder="templates")
import requests
import webbrowser


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "y4L1Z37QDgTZex4svMbmqUh9KHksM84TAoWkcKbCnj9x"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
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
    input_arr = [[int(gender_num), float(ssc_p), int(ssc_b_num), float(hsc_p), int(hsc_b_num), int(hsc_s_num), float(degree_p), int(degree_t_num), int(workex_num), float(etest_p), int(specialisation_num), float(mba_p)]]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [[int(gender_num), float(ssc_p), int(ssc_b_num), float(hsc_p), int(hsc_b_num), int(hsc_s_num), float(degree_p), int(degree_t_num), int(workex_num), float(etest_p), int(specialisation_num), float(mba_p)]], "values": input_arr}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a18437a4-857c-4507-a6f0-6230446daff6/predictions?version=2021-05-01', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions=response_scoring.json()
    output=predictions['predictions'][0]['values'][0][0]
    print("final prediction ",output)
    print(output) 
      
    return render_template('out.html')
if __name__ == "__main__":
    # Run the app
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
