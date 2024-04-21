from flask import Flask, render_template, request
import pickle
import numpy as np
import json
import os

app = Flask(__name__)

# Load the model
model_file = "C:\\Users\\vibhor\\Desktop\\ai_pro\\BANGALORE-HOUSE-PRICE-PREDICTION\\BHPP\\banglore_home_prices_model.pickle"
with open(model_file, 'rb') as f:
    model = pickle.load(f)

# Load the columns
columns_file = "C:\\Users\\vibhor\\Desktop\\ai_pro\\BANGALORE-HOUSE-PRICE-PREDICTION\\BHPP\\columns.json"
if os.path.exists(columns_file):
    with open(columns_file, 'r') as f:
        data = json.load(f)
        __data_columns = data['data_columns']
        __locations = __data_columns[3:]
else:
    print(f"Error: '{columns_file}' not found. Please make sure the file exists.")

def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['location'].lower())
    except ValueError:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = input_json['sqft']
    x[1] = input_json['bath']
    x[2] = input_json['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(model.predict([x])[0], 2)
    return result

@app.route('/')
def index():
    return render_template('index.html', locations=__locations)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        input_json = {
            "location": request.form['sLocation'],
            "sqft": float(request.form['Squareft']),
            "bhk": int(request.form['uiBHK']),
            "bath": int(request.form['uiBathrooms'])
        }
        result = get_estimated_price(input_json)

        if result > 100:
            result = round(result / 100, 2)
            result = str(result) + ' Crore'
        else:
            result = str(result) + ' Lakhs'

    return render_template('predict.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
