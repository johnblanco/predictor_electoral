import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib

QUESTIONS_COUNT = 27


def resp(id_encuesta, id_pregunta):
    s = respuestas[
        (respuestas["id_encuesta"] == id_encuesta)
        & (respuestas["id_pregunta"] == id_pregunta)
    ]["respuesta"]
    return s.get_values()[0]


n = 17
k = 7

pca = PCA(n_components=n)

# para generar los csvs correr primero export_db
df = pd.read_csv("../csvs/encuestas_original.csv")
respuestas = pd.read_csv("../csvs/respuestas_encuestas_original.csv")

for i in range(1, QUESTIONS_COUNT):
    df["resp_{}".format(i)] = df.id.apply(lambda x: resp(x, i))

features = []
for i in range(1, QUESTIONS_COUNT):
    features.append("resp_{}".format(i))

pca.fit(df[features])
X = pca.transform(df[features])
y = df.candidato
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
candidate_model = KNeighborsClassifier(n_neighbors=n)
candidate_model.fit(X_train, y_train)

df_train, df_test = train_test_split(df, test_size=0.20)
df_test["kn_candidate_prediction"] = candidate_model.predict(
    pca.transform(df_test[features])
)
ok = len(df_test[df_test.kn_candidate_prediction == df_test.candidato])
precision = ok / len(df_test)
print("precision candidato: {}".format(precision))

# exporto modelos
joblib.dump(pca, "../predictor_pol/pca.joblib")
joblib.dump(candidate_model, "../predictor_pol/candidate_model.joblib")

# pruebo que la importacion funcione bien


pcax = joblib.load("../predictor_pol/pca.joblib")

d = {
    "resp_21": ["1"],
    "resp_1": ["1"],
    "resp_23": ["1"],
    "resp_24": ["1"],
    "resp_11": ["1"],
    "resp_9": ["1"],
    "resp_13": ["1"],
    "resp_14": ["1"],
    "resp_10": ["1"],
    "resp_22": ["1"],
    "resp_5": ["1"],
    "resp_16": ["1"],
    "resp_3": ["1"],
    "resp_18": ["1"],
    "resp_2": ["1"],
    "resp_8": ["1"],
    "resp_12": ["1"],
    "resp_19": ["1"],
    "resp_17": ["1"],
    "resp_26": ["1"],
    "resp_20": ["1"],
    "resp_4": ["1"],
    "resp_25": ["1"],
    "resp_15": ["1"],
    "resp_6": ["1"],
    "resp_7": ["1"],
}
foo = pd.DataFrame.from_dict(d)

bar = pcax.transform(foo)
print(candidate_model.predict(bar))  # 3
