# Import
from crypt import methods
from os import pipe
from flask import Flask, request
import pickle
# from flask_restful import Api
import pandas as pd
from sklearn import pipeline
from  data_prep import classifica_mnb

# modelmnb = pickle.load(open('/home/recruta/github/multinomialNB/classifica_mnb.pkl','rb'))

# Instanciate Flask
app = Flask(__name__)

@app.route('/predict', methods=['POST'])

def predict():
    data_json = request.get_json()

    # Collect data
    if data_json:
        df_data = [data_json]
#        if isinstance( data_json, list):
#            df_data = pd.DataFrame(data_json, index=[0])
#       else:
#            df_data = pd.DataFrame(data_json, columns=data_json[0].keys())
    
    # Instanciate data preparation
    pipeline = classifica_mnb()

    # Data preparation and predict
    pred = pipeline.mnb_predict(str(df_data[0][:]))

    df_data['prediction'] = pred

    return df_data.to_json(orient='records')

if __name__ == '__main__':
    # Start Flask
    app.run(host='0.0.0.0', port='5000')

