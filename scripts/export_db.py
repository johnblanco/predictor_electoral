# estos csv se guardan en la carpeta csvs, pero no se dejan en github, estan en https://www.dropbox.com/sh/dpzxb1hwq6n26qh/AAB-HMaoQqEF6l7ZuUtSy5sAa?dl=0

import sqlite3
import pandas as pd

db = sqlite3.connect("../predictor_pol/predictor_prod.db", isolation_level=None)
sql = """
select id,candidato_elegido,fecha
from encuestas where candidato_elegido is not null;
"""

cur = db.cursor()
rows = cur.execute(sql).fetchall()

with open("../csvs/encuestas.csv", "w") as f:
    f.write("id,candidato,fecha\n")
    for r in rows:
        f.write(f"{r[0]},{r[1]},{r[2]}\n")


sql = """
select id_encuesta,id_pregunta,respuesta
from respuestas_encuestas;
"""

cur = db.cursor()
rows = cur.execute(sql).fetchall()

with open("../csvs/respuestas_encuestas.csv", "w") as f:
    f.write("id_encuesta,id_pregunta,respuesta\n")
    for r in rows:
        f.write(f"{r[0]},{r[1]},{r[2]}\n")


sql = """
select id as cant,fecha
from encuestas
where fecha > '2019-02-17'
"""

cur = db.cursor()
rows = cur.execute(sql).fetchall()

d = {"cant": [], "fecha": []}
for r in rows:
    d["cant"].append(r[0])
    d["fecha"].append(r[1])

df = pd.DataFrame.from_dict(d)
df["dia"] = df.fecha.apply(lambda x: x[0:10])
by_day = df.groupby("dia").count()[["cant"]]
by_day.to_csv("../csvs/encuestas_por_dia.csv")
