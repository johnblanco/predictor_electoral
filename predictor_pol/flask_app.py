# para correr: export FLASK_APP=flask_app.py;flask run

import datetime
import joblib
import json
import pandas as pd
import sqlite3
import os
from flask import Flask, render_template, request, g, session, redirect
from sklearn.decomposition import PCA

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
            'party': party['party'].title(),
            'candidates': []
            })
        for candidate in party['candidates']:
            CANDIDATOS[-1]['candidates'].append({
            	'name': candidate['name'].title(),
            	'id': candidate['id']
            	}) 

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

@app.route('/update_quiz', methods=['POST'])
def add_mail():
    if request.method == 'POST':
        update_quiz(request.form, int(session['answer_id']))
        return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        session['page'] += 1
        for key, value in request.form.items():
            session[key] = value

        for category in PREGUNTAS:
            for question in category['questions']:
                if question['id'] not in session:
                    return render_template(
                        'questions.html',
                        preguntas=[category],
                        respuestas=RESPUESTAS,
                        page=session['page']
                    )

        if validate(session):
            predictions = predict(session)
            answer_id = save_response(session, predictions['candidate_id'])
            session['answer_id'] = answer_id

            return render_template('success.html',
                                   predicted_candidate_name=predictions['candidate_name'],
                                   candidatos = CANDIDATOS)
        else:
            # Esto también
            return 'Error'

    session.clear()
    session['page'] = 0
    return render_template(
        'main.html'
    )


def validate(form):
    valid_keys = {
        *_get_question_keys(PREGUNTAS)
    }
    return all(form.get(key, '').isdecimal() for key in valid_keys)


def predict(responses):
    candidate_model = joblib.load(PATH + 'candidate_model.joblib')

    d = {}
    for i in range(1,27):
        d['resp_{}'.format(i)] = [ responses['pregunta_{}'.format(i)] ]
    print(d)
    df = pd.DataFrame.from_dict(d)
    pca = PCA(n_components=12)
    pca.fit(df)
    candidate_id = candidate_model.predict(pca.transform(df))
    print(candidate_id)

    candidate_name = ''
    for p in CANDIDATOS:
        for c in p['candidates']:
            if c['id'] == candidate_id:
                candidate_name = c['name']
    return {'candidate_id': candidate_id, 'candidate_name': candidate_name}


def update_quiz(form, id):
    cur = get_db().cursor()
    sql = (
            "update encuestas set email=?, candidato_elegido=?"
            "where id=?;"
        )

    email = form['email']
    candidato = int(form['candidato'])
    cur.execute(sql, (email,candidato, id))

def save_response(form, predicted_candidate_id):
    fecha = datetime.datetime.now().isoformat()
    cur = get_db().cursor()
    sql = (
        "insert into encuestas('fecha','candidato_predicho')"
        "values(?,?);"
    )
    res = cur.execute(sql, (fecha, predicted_candidate_id))
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
