import pickle
import pandas as pd
import sys
sys.path.insert(1,'/home/recruta/Documentos/GitHub/phrase_analyser/app')

from handler import classifica_mnb
from crypt import methods
from flask import Flask
from flask import request
from numpy import record
from sklearn import pipeline

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data_json = request.get_json()

    if data_json:
        isinstance(data_json,list)
        x_json=[data_json['phrase']]

    # Instance classifica_mnb   
    pipeline=classifica_mnb()

    # Preparation
    transformVector = pipeline.preparation(x_json)

    # Predict
    predictVector = pipeline.prediction(transformVector)

    # PredictProba
    predictProba = pipeline.predictionProba(transformVector)

    # Result
    result_proba = pipeline.resultPrediction(predictProba)

    # Save phrase and prediction
    saveData = pd.DataFrame()
    saveData['phrase'].append(x_json)
    saveData['predict'].append(predictVector)
    saveData['probability_negative'] = predictProba[0][0]
    saveData['probability_positive'] = predictProba[0][1]
    saveData.to_csv('/home/recruta/Documentos/GitHub/phrase_analyser/app/inventory/newData.csv')

    # Return json
    data_json = pd.DataFrame()
    data_json['predict'] = predictVector
    data_json['probability_negative'] = predictProba[0][0]
    data_json['probability_positive'] = predictProba[0][1]
    data_json['result']= str(result_proba)
    return data_json.to_json(orient='records')

# Instance Flask
if __name__ == '__main__':
    # Start Flask
    app.run(host='0.0.0.0' , port=5000)