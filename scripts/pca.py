import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import json

df = pd.read_csv('../csvs/encuestas.csv')
cand_data = json.loads(open('../predictor_pol/candidatos.json','r').read())

def get_party(id):
    for p in cand_data:
        for c in p['candidates']:
            if c['id'] == id:
                return p['party']
    return 'n/a'

def get_name(id):
    for p in cand_data:
        for c in p['candidates']:
            if c['id'] == id:
                return c['name']
    return 'n/a'

df['partido'] = df.candidato.apply(get_party)
df['nombre'] = df.candidato.apply(get_name)

respuestas = pd.read_csv('../csvs/respuestas_encuestas.csv')

def resp(id_encuesta,id_pregunta):
    s= respuestas[(respuestas['id_encuesta'] == id_encuesta) & (respuestas['id_pregunta'] == id_pregunta)]['respuesta']
    return s.get_values()[0]

for i in range(1,27):
    df['resp_{}'.format(i)] = df.id.apply(lambda x: resp(x,i))

features = []
for i in range(1,27):
    features.append('resp_{}'.format(i))


scores_candidatos = []
for n in range(2,20):
    pca = PCA(n_components=n)
    pca.fit(df[features])
    X = pca.transform(df[features])
    y = df.candidato
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    for k in range(1,15):
        modelo = KNeighborsClassifier(n_neighbors=k)
        modelo.fit(X_train, y_train)
        s = modelo.score(X_test, y_test)
        scores_candidatos.append([s, n, k])

print(max(scores_candidatos))

scores_partidos = []
for n in range(2,20):
    pca = PCA(n_components=n)
    pca.fit(df[features])
    X = pca.transform(df[features])
    y = df.partido
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    for k in range(1,15):
        modelo = KNeighborsClassifier(n_neighbors=k)
        modelo.fit(X_train, y_train)
        s = modelo.score(X_test, y_test)
        scores_partidos.append([s, n, k])

print(max(scores_partidos))
