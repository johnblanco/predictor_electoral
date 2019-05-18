import pandas as pd
from load_data import CANDIDATOS, RESPUESTAS_CANDIDATOS, QUESTIONS_COUNT


def calculate_coincidence(sum, count):
    return (1 - (sum/(7 * count))) * 100

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
    coincidence_percentages = []
    df = RESPUESTAS_CANDIDATOS
    for index, candidate in df.iterrows():
        id = candidate["candidate_id"]
        name = candidate["candidate_name"]
        sum = 0
        for i in range(1, QUESTIONS_COUNT + 1):
            j = i + 1
            sum += abs(int(responses["pregunta_" + str(i)]) - candidate["question_" + str(j)])
        coincidence_percentages.append([id, name, calculate_coincidence(sum, QUESTIONS_COUNT)])
    coincidence_percentages.sort(key=lambda x:x[2], reverse=True)
    politicians_model_response = {
        "candidate_id": coincidence_percentages[0][0],
        "candidate_name": coincidence_percentages[0][1],
        "coincidence_percentage": round(coincidence_percentages[0][2])
    }
    print(politicians_model_response)
    # en la primer salida vamos a tener solo politicians_model y None en people_model
    # porque hay que reentrenar con las nuevas preguntas
    res = {"people_model": None, "politicians_model": politicians_model_response}

    return res
