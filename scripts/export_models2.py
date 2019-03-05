import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import joblib
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("../csvs/data.csv")
df_train, df_test = train_test_split(df, test_size=0.20)
l = list(range(1, 27))
features = list(map(lambda x: str(x), l))


clf = LogisticRegression(
    random_state=0, solver="lbfgs", multi_class="multinomial", max_iter=700
).fit(df_train[features], df_train.candidatoId)
joblib.dump(clf, "../predictor_pol/candidate_model2.joblib")
