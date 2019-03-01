#estos csv se guardan en la carpeta actual, pero no se dejan en github, estan en https://www.dropbox.com/sh/dpzxb1hwq6n26qh/AAB-HMaoQqEF6l7ZuUtSy5sAa?dl=0

import sqlite3

db = sqlite3.connect("../predictor_pol/predictor_prod.db", isolation_level=None)
sql = """
select id,candidato_elegido,fecha
from encuestas where candidato_elegido is not null;
"""

cur = db.cursor()
rows = cur.execute(sql).fetchall()

with open("encuestas.csv", "w") as f:
    f.write("id,candidato,fecha\n")
    for r in rows:
        f.write(f"{r[0]},{r[1]},{r[2]}\n")


sql = """
select id_encuesta,id_pregunta,respuesta
from respuestas_encuestas;
"""

cur = db.cursor()
rows = cur.execute(sql).fetchall()

with open("respuestas_encuestas.csv", "w") as f:
    f.write("id_encuesta,id_pregunta,respuesta\n")
    for r in rows:
        f.write(f"{r[0]},{r[1]},{r[2]}\n")
