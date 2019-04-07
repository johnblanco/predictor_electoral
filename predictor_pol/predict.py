from load_data import CANDIDATOS


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
    candidate_name = ""
    candidate_id = 20  # test
    for party in CANDIDATOS:
        for candidate in party["candidates"]:
            if candidate["id"] == candidate_id:
                candidate_name = candidate["name"]
    politicians_model_response = {
        "candidate_id": candidate_id,
        "candidate_name": candidate_name,
    }
    # en la primer salida vamos a tener solo politicians_model y None en people_model
    # porque hay que reentrenar con las nuevas preguntas
    res = {"people_model": None, "politicians_model": politicians_model_response}

    return res
