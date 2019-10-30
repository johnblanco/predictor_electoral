import json
import os

PATH = os.path.dirname(os.path.realpath(__file__)) + "/"


DATABASE = PATH + "predictor_prod.db"
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

with open(PATH + "candidatos.json") as f:
    CANDIDATOS = json.load(f)

with open(PATH + "respuestas.json") as f:
    RESPUESTAS = json.load(f)

with open(PATH + "secrets.json") as f:
    secrets = json.load(f)
    RECAPTCHA_SECRET_KEY = secrets.get("RECAPTCHA_SECRET_KEY")
