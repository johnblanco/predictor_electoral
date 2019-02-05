# para correr: export FLASK_APP=flask_app.py;flask run

import datetime
import joblib
import json
import pandas as pd
import sqlite3
import os
from flask import Flask, render_template, request, g, session, redirect

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
    CANDIDATOS = []
    file_parties = json.load(f)
    for party in file_parties:
        CANDIDATOS.append({
            'name': party['name'].title(),
            'candidates': []
            })
        for candidate in party['candidates']:
            CANDIDATOS[-1]['candidates'].append(candidate) 

with open(PATH + 'respuestas.json') as f:
    RESPUESTAS = json.load(f)

DATABASE = PATH + 'predictor_prod.db'


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

@app.route('/count_rows', methods=['GET'])
def count_rows():
    cur = get_db().cursor()
    sql = 'select count(1) from encuestas;'
    rows = cur.execute(sql).fetchall()

    return str(rows[0][0])

@app.route('/add-mail', methods=['POST'])
def add_mail():
    if request.method == 'POST':
        print(request.form)
        print(int(session['answer_id']))
        save_email(request.form, int(session['answer_id']))
        return redirect('/')

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
            answer_id = save_response(session)
            session['answer_id'] = answer_id
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


def save_email(form,id):
    cur = get_db().cursor()
    sql = (
            "update encuestas set email=?"
            "where id=?;"
        )
    cur.execute(sql, (form['email'], id))

def save_response(form):
    fecha = datetime.datetime.now().isoformat()
    cur = get_db().cursor()
    candidato = int(form['candidato'])
    sql = (
        "insert into encuestas('candidato_elegido','fecha')"
        "values(?,?);"
    )
    res = cur.execute(sql, (candidato, fecha))
    id_encuesta = int(res.lastrowid)

    for id_pregunta in _get_question_keys(PREGUNTAS):
        respuesta = int(form[id_pregunta])

        sql = (
            "insert into respuestas_encuestas"
            "('id_encuesta','id_pregunta','respuesta') values(?,?,?);"
        )
        cur.execute(sql, (id_encuesta, id_pregunta.split('_')[-1], respuesta))

    return id_encuesta


def _get_question_keys(questions):
    return [
        question['id']
        for category in questions
        for question in category['questions']
    ]
