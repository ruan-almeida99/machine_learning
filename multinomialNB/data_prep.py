import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

class classifica_mnb(object):
    def __init__(self):
        self.model_mnb = pickle.load(open('/home/recruta/github/multinomialNB/model_mnb.pkl','rb'))
        self.vectorizer= pickle.load(open('/home/recruta/github/multinomialNB/vectorizer_transform.pkl','rb'))

    def mnb_predict(self, x:str):
        # Transform
        x = [x]
        vectorizer2 = self.vectorizer
        y = vectorizer2.transform(x).toarray()
        pred = self.model_mnb.predict(y)
        pred_prob = self.model_mnb.predict_proba(y)
    
        print(x, "Predição:",pred[0],"\n")
        if pred == 1 and pred_prob[0][1]>0.5:print("A frase foi classificada como positiva!\nCom a probabilidade de ser %",round(pred_prob[0][1]*100,2),"positiva!")
        elif pred_prob[0][0] and pred_prob[0][1] == 0.5:print("Não é possivél determinar!")
        else:print("A frase foi classificada como negativa!\nCom a probabilidade de ser %",round(pred_prob[0][0]*100,2),"negativa!")