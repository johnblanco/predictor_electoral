# para correr: export FLASK_APP=flask_app.py;flask run

import datetime
import joblib
import json
import pandas as pd
import sqlite3
import os
from flask import Flask, render_template, request, g

app = Flask(__name__)
path = os.path.dirname(os.path.realpath(__file__))

with open(path + 'preguntas.json') as f:
    PREGUNTAS = [
        question
        for category in json.load(f)
        for question in category['questions']
    ]

with open(path + 'candidatos.json') as f:
    CANDIDATOS = [
        candidate
        for pol_party in json.load(f)
        for candidate in pol_party['candidates']
    ]

DATABASE = path + 'predictor.db'
MODELO_LISTO = False


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    return db


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        if validate(request.form):
            save_response(request)
            return render_template('success.html')
        else:
            # Esto también
            return 'Error'

    return render_template(
        'main.html',
        preguntas=PREGUNTAS,
        candidatos=CANDIDATOS,
        modelo_listo=MODELO_LISTO
    )


def validate(form):
    valid_keys = {
        'candidato',
        *_get_question_keys(PREGUNTAS)
    }
    return all(form.get(key, '').isdecimal() for key in valid_keys)


def predict(responses):
    xgb = joblib.load('xg_model')
    df_test = pd.DataFrame.from_dict({'resp1': [1], 'resp2': [1]})
    print(xgb.predict(df_test))


def save_response(request):
    form = request.form
    ip = request.remote_addr
    fecha = datetime.datetime.now().isoformat()
    cur = get_db().cursor()
    candidato = int(form['candidato'])
    sql = (
        "insert into encuestas('candidato_elegido','ip','fecha')"
        "values(?,?,?);"
    )
    res = cur.execute(sql, (candidato, ip, fecha))
    id_encuesta = int(res.lastrowid)

    for id_pregunta in _get_question_keys(PREGUNTAS):
        respuesta = int(form[id_pregunta])

        sql = (
            "insert into respuestas_encuestas"
            "('id_encuesta','id_pregunta','respuesta') values(?,?,?);"
        )
        cur.execute(sql, (id_encuesta, id_pregunta.split('_')[-1], respuesta))


def _get_question_keys(questions):
    return ['pregunta_{}'.format(i + 1) for i, _ in enumerate(questions)]
