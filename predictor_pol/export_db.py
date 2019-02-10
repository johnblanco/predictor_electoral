import sqlite3

db = sqlite3.connect('predictor_prod.db', isolation_level=None)
sql = '''
select id,candidato_elegido,fecha
from encuestas;
'''

cur = db.cursor()
rows = cur.execute(sql).fetchall()

with open('encuestas.csv','w') as f:
    f.write('id,candidato,fecha\n')
    for r in rows:
        f.write('{},{},{}\n'.format(r[0],r[1],r[2]))


sql = '''
select id_encuesta,id_pregunta,respuesta
from respuestas_encuestas;
'''

cur = db.cursor()
rows = cur.execute(sql).fetchall()

with open('respuestas_encuestas.csv','w') as f:
    f.write('id_encuesta,id_pregunta,respuesta\n')
    for r in rows:
        f.write('{},{},{}\n'.format(r[0],r[1],r[2]))