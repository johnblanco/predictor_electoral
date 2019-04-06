# para correr: export FLASK_APP=flask_app.py;flask run

import datetime
import joblib
import requests
import pandas as pd
import sqlite3

from flask import Flask, render_template, request, g, session, redirect
from load_data import (
    DATABASE,
    PREGUNTAS,
    CANDIDATOS,
    PATH,
    QUESTIONS_COUNT,
    RESPUESTAS,
    RECAPTCHA_SECRET_KEY,
)

RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    return db


@app.route("/count_rows", methods=["GET"])
def count_rows():
    cur = get_db().cursor()
    sql = "select count(1) from encuestas;"
    rows = cur.execute(sql).fetchall()

    return str(rows[0][0])


@app.route("/update_quiz", methods=["POST"])
def add_mail():
    if request.method == "POST":
        update_quiz(request.form, int(session["answer_id"]))
        return redirect("/")


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        if session["page"] == len(PREGUNTAS):
            if not validate_captcha(request.form.get("g-recaptcha-response")):
                return (
                    "No pudimos verificar que seas humano.\n"
                    "Beep boop. Hola señor robot."
                )

        session["page"] += 1
        for key, value in request.form.items():
            session[key] = value

        for category in PREGUNTAS:
            for question in category["questions"]:
                if question["id"] not in session:
                    return render_template(
                        "questions.html",
                        num_categories=len(PREGUNTAS),
                        preguntas=[category],
                        respuestas=RESPUESTAS,
                        page=session["page"],
                    )

        if validate(session):
            predictions = predict(session)
            answer_id = save_response(session)
            session["answer_id"] = answer_id

            return render_template(
                "success.html",
                predictions=predictions,
                candidatos=CANDIDATOS,
            )
        else:
            # Esto también
            return "Error"

    session.clear()
    session["page"] = 0
    return render_template("main.html")


def validate_captcha(captcha_response):
    if captcha_response is None:
        return False

    validation_response = requests.post(
        RECAPTCHA_URL,
        data={"secret": RECAPTCHA_SECRET_KEY, "response": captcha_response},
    )
    return validation_response.json().get("success")


def validate(form):
    valid_keys = {*_get_question_keys(PREGUNTAS)}
    return all(form.get(key, "").isdecimal() for key in valid_keys)


def predict(responses):
    # candidate_model = joblib.load(PATH + "candidate_model2.joblib")
    #
    # d = {}
    # for i in range(1, QUESTIONS_COUNT + 1):
    #     d[f"resp_{i}"] = [responses[f"pregunta_{i}"]]
    #
    # df = pd.DataFrame.from_dict(d)
    #
    # candidate_id = candidate_model.predict(df)
    #
    candidate_name = ""
    candidate_id = 20 #test
    for party in CANDIDATOS:
        for candidate in party["candidates"]:
            if candidate["id"] == candidate_id:
                candidate_name = candidate["name"]
    politicians_model_response = {'candidate_id': candidate_id, 'candidate_name': candidate_name}
    #en la primer salida vamos a tener solo politicians_model y None en people_model porque hay que reentrenar con las
    #nuevas preguntas
    res = {'people_model': None, "politicians_model": politicians_model_response}

    return res


def update_quiz(form, id):
    cur = get_db().cursor()
    sql = "update encuestas set candidato_elegido=? where id=?;"

    candidato = int(form["candidato"])
    cur.execute(sql, (candidato, id))


def save_response(form):
    fecha = datetime.datetime.now().isoformat()
    cur = get_db().cursor()
    sql = "insert into encuestas('fecha','version') values(?,?);"
    res = cur.execute(sql, (fecha, 2))
    id_encuesta = int(res.lastrowid)

    for id_pregunta in _get_question_keys(PREGUNTAS):
        respuesta = int(form[id_pregunta])

        sql = (
            "insert into respuestas_encuestas"
            "('id_encuesta','id_pregunta','respuesta') values(?,?,?);"
        )
        cur.execute(sql, (id_encuesta, id_pregunta.split("_")[-1], respuesta))

    return id_encuesta


def _get_question_keys(questions):
    return [
        question["id"] for category in questions for question in category["questions"]
    ]
