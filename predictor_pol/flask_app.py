# para correr: export FLASK_APP=flask_app.py;flask run

import datetime
import joblib
import json
import pandas as pd
import sqlite3
import os
from flask import Flask, render_template, request, g, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

with open(PATH + 'preguntas.json') as f:
    PREGUNTAS = []
    # create the dict structure for the questions constant
    file_questions = json.load(f)
    index = 1
    for category in file_questions:
        PREGUNTAS.append({
            'subject': category['subject'].title(),
            'questions': []
        })
        for question in category['questions']:
            PREGUNTAS[-1]['questions'].append({
                'text': question,
                'id': 'pregunta_{}'.format(index)
            })
            index += 1


with open(PATH + 'candidatos.json') as f:
    CANDIDATOS = [
        candidate
        for pol_party in json.load(f)
        for candidate in pol_party['candidates']
    ]

with open(PATH + 'respuestas.json') as f:
    RESPUESTAS = json.load(f)

DATABASE = PATH + 'predictor.db'


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
        for key, value in request.form.items():
            session[key] = value

        for category in PREGUNTAS:
            for question in category['questions']:
                if question['id'] not in session:
                    return render_template(
                        'questions.html',
                        preguntas=[category],
                        respuestas=RESPUESTAS
                    )

        if validate(session):
            save_response(session)
            return render_template('success.html')
        else:
            # Esto también
            return 'Error'

    session.clear()
    return render_template(
        'main.html',
        candidatos=CANDIDATOS
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


def save_response(form):
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
    return [
        question['id']
        for category in questions
        for question in category['questions']
    ]
