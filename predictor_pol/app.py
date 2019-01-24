#para correr: export FLASK_APP=app.py;flask run

from flask import Flask, render_template, request
import joblib
import pandas as pd


app = Flask(__name__)

preguntas = ['Pregunta 1', 'Pregunta 2']
candidatos = ['Candidato 1', 'Candidato 2', 'Juan Sartori (aka u/nano2412)']
valid_keys = {
    'candidato',
    *('pregunta_' + str(i) for i in range(1, len(preguntas)))
}


@app.route('/', methods = ['GET', 'POST'])
def main():
    if request.method == 'POST':
        if validate(request.form):
            print(request.form)
            # Esto habría que reemplazar por un render_template
            return 'Gracias por contestar!'
        else:
            # Esto también
            return 'Error'

    return render_template('main.html', preguntas=preguntas, candidatos=candidatos)


def validate(form):
    return all(form.get(key, '').isdecimal() for key in valid_keys)


def predict(responses):
    xgb = joblib.load('xg_model')
    df_test = pd.DataFrame.from_dict({'resp1': [1], 'resp2': [1]})
    print(xgb.predict(df_test))
