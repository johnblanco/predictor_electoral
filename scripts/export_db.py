# estos csv se guardan en la carpeta csvs, pero no se dejan en github
# estan en https://www.dropbox.com/sh/dpzxb1hwq6n26qh/AAB-HMaoQqEF6l7ZuUtSy5sAa?dl=0

import sqlite3
import pandas as pd

NUM_QUESTIONS = 26

db = sqlite3.connect("../predictor_pol/predictor_prod.db", isolation_level=None)
cur = db.cursor()


sql = """
    SELECT
        encuestas.id,
        encuestas.candidato_elegido,
        group_concat(resp.id_pregunta || ":" || resp.respuesta),
        encuestas.fecha
    FROM respuestas_encuestas as resp
    JOIN encuestas ON encuestas.id == resp.id_encuesta
    WHERE encuestas.candidato_elegido in (4,9)
    GROUP BY resp.id_encuesta
    """
rows = cur.execute(sql).fetchall()

with open("../csvs/data.csv", "w") as f:
    all_questions = ",".join([str(i) for i in range(1, NUM_QUESTIONS + 1)])
    f.write(f"id,candidatoId,{all_questions},fecha\n")

    for r in rows:
        id_encuesta = r[0]
        id_candidato = r[1]
        fecha_encuesta = r[3]

        respuestas = r[2].split(",")
        if len(respuestas) < NUM_QUESTIONS:
            continue
        respuestas.sort(key=lambda x: int(x.split(":")[0]))
        respuestas = ",".join([respuesta.split(":")[1] for respuesta in respuestas])

        f.write(f"{id_encuesta},{id_candidato},{respuestas},{fecha_encuesta}\n")


sql = """
SELECT id AS cant,fecha
FROM encuestas
WHERE fecha > '2019-02-17'
"""

rows = cur.execute(sql).fetchall()

d = {"cant": [row[0] for row in rows], "fecha": [row[1] for row in rows]}

df = pd.DataFrame.from_dict(d)
df["dia"] = df.fecha.apply(lambda x: x[0:10])
by_day = df.groupby("dia").count()[["cant"]]
by_day.to_csv("../csvs/encuestas_por_dia.csv")
