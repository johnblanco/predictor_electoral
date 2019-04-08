import json
import os

PATH = os.path.dirname(os.path.realpath(__file__)) + "/json_data/"


DATABASE = PATH + "../predictor_prod.db"
with open(PATH + "preguntas.json") as f:
    PREGUNTAS = []
    # create the dict structure for the questions constant
    file_questions = json.load(f)
    index = 1
    for category in file_questions:
        PREGUNTAS.append({"subject": category["subject"].title(), "questions": []})
        for question in category["questions"]:
            PREGUNTAS[-1]["questions"].append(
                {"text": question, "id": "pregunta_{}".format(index)}
            )
            index += 1

QUESTIONS_COUNT = sum([len(category["questions"]) for category in PREGUNTAS])

QUESTION_KEYS = [
    question["id"] for category in PREGUNTAS for question in category["questions"]
]

with open(PATH + "candidatos.json") as f:
    CANDIDATOS = []
    file_parties = json.load(f)
    for party in file_parties:
        CANDIDATOS.append({"party": party["party"].title(), "candidates": []})
        for candidate in party["candidates"]:
            CANDIDATOS[-1]["candidates"].append(
                {"name": candidate["name"].title(), "id": candidate["id"]}
            )

with open(PATH + "respuestas.json") as f:
    RESPUESTAS = json.load(f)

with open(PATH + "secrets.json") as f:
    secrets = json.load(f)
    RECAPTCHA_SECRET_KEY = secrets.get("RECAPTCHA_SECRET_KEY")
    RECAPTCHA_SITE_KEY = secrets.get("RECAPTCHA_SITE_KEY")
