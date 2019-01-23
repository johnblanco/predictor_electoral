#para correr: export FLASK_APP=app.py;flask run

from flask import Flask
from flask import render_template
from flask import request
import joblib
import pandas as pd

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def main():
    if request.method == 'POST':
        print(request.form)

    preguntas = [{'id': 1, 'texto': 'pregunta 1'},{'id': 2, 'texto': 'pregunta 2'}]
    candidatos = [{'id': 1, 'nombre': 'candidato 1'},{'id': 2, 'nombre': 'candidato 2'}]

    return render_template('main.html', preguntas=preguntas, candidatos=candidatos)

def predict(responses):
    xgb = joblib.load('xg_model')
    df_test = pd.DataFrame.from_dict({'resp1': [1], 'resp2': [1]})
    print(xgb.predict(df_test))
