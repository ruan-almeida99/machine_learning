from unittest import result
import pandas
import numpy as np
import pickle

class classifica_mnb(object):
    def __init__(self):
        self.model_mnb=pickle.load(open('/home/recruta/Documentos/GitHub/phrase_analyser/app/inventory/model_mnb.pkl','rb'))
        self.vectorizer=pickle.load(open('/home/recruta/Documentos/GitHub/phrase_analyser/app/inventory/vectorizer.pkl','rb'))

    def preparation(self,textTransform:list):
        y = self.vectorizer.transform(textTransform).toarray()
        return y

    def prediction(self,vector):
        pred = self.model_mnb.predict(vector)
        return pred

    def predictionProba(self, vector):  
        pred_prob = self.model_mnb.predict_proba(vector)
        return pred_prob
    
    def resultPrediction(self,pred_proba):
        if pred_proba[0][1] >0.5:result_proba='Frase Positiva.'
        elif pred_proba[0][1] == 0.5:result_proba='Não é possivel determinar.'
        else:result_proba='Frase negativa'
        return result_proba