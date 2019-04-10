import datetime
import sqlite3

from load_data import DATABASE, QUESTION_KEYS
from flask import g


def close_connection():
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    return db


def update_quiz(form, id):
    cur = get_db().cursor()
    sql = "UPDATE encuestas SET candidato_elegido=? WHERE id=?;"

    candidato = int(form["candidato"])
    cur.execute(sql, (candidato, id))


def save_response(form):
    fecha = datetime.datetime.now().isoformat()
    cur = get_db().cursor()
    sql = "INSERT INTO encuestas ('fecha','version') VALUES(?,?);"
    res = cur.execute(sql, (fecha, 2))
    id_encuesta = int(res.lastrowid)

    for id_pregunta in QUESTION_KEYS:
        respuesta = int(form[id_pregunta])

        sql = (
            "INSERT INTO respuestas_encuestas"
            "('id_encuesta','id_pregunta','respuesta') VALUES(?,?,?);"
        )
        cur.execute(sql, (id_encuesta, id_pregunta.split("_")[-1], respuesta))

    return id_encuesta


def count_rows():
    cur = get_db().cursor()
    sql = "SELECT count(1) FROM encuestas;"
    rows = cur.execute(sql).fetchall()
    return str(rows[0][0])
