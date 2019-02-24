import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib


QUESTIONS_COUNT = 26
N = 17
K = 7


def resp(id_encuesta, id_pregunta):
    s = respuestas[
        (respuestas["id_encuesta"] == id_encuesta)
        & (respuestas["id_pregunta"] == id_pregunta)
    ]["respuesta"]
    return s.get_values()[0]


if __name__ == "__main__":
    pca = PCA(n_components=N)

    # para generar los csvs correr primero export_db
    df = pd.read_csv("../csvs/encuestas_original.csv")
    respuestas = pd.read_csv("../csvs/respuestas_encuestas_original.csv")

    for i in range(1, QUESTIONS_COUNT + 1):
        df[f"resp_{i}"] = df.id.apply(lambda x: resp(x, i))

    features = [f"resp_{i}" for i in range(1, QUESTIONS_COUNT + 1)]

    pca.fit(df[features])
    X = pca.transform(df[features])
    y = df.candidato
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    candidate_model = KNeighborsClassifier(n_neighbors=N)
    candidate_model.fit(X_train, y_train)

    df_train, df_test = train_test_split(df, test_size=0.20)
    df_test["kn_candidate_prediction"] = candidate_model.predict(
        pca.transform(df_test[features])
    )
    ok = len(df_test[df_test.kn_candidate_prediction == df_test.candidato])
    precision = ok / len(df_test)
    print(f"precision candidato: {precision}")

    # exporto modelos
    joblib.dump(pca, "../predictor_pol/pca.joblib")
    joblib.dump(candidate_model, "../predictor_pol/candidate_model.joblib")

    # pruebo que la importacion funcione bien

    pcax = joblib.load("../predictor_pol/pca.joblib")

    d = {f"resp_{i}": ["1"] for i in range(1, QUESTIONS_COUNT + 1)}
    foo = pd.DataFrame.from_dict(d)

    bar = pcax.transform(foo)
    print(candidate_model.predict(bar))
