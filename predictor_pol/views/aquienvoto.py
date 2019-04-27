import requests

from flask import Blueprint, request, session, redirect, render_template

import db_manager


from load_data import (
    PREGUNTAS,
    CANDIDATOS,
    QUESTION_KEYS,
    RESPUESTAS,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY
)
from predict import predict

RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"

bp = Blueprint("aquienvoto_bp", __name__, template_folder="templates", url_prefix="/")


def validate_captcha(captcha_response):
    if captcha_response is None:
        return False

    validation_response = requests.post(
        RECAPTCHA_URL,
        data={"secret": RECAPTCHA_SECRET_KEY, "response": captcha_response},
    )
    return validation_response.json().get("success")


@bp.route("/count_rows", methods=["GET"])
def count_rows():
    return db_manager.count_rows()

@bp.route("/test_success", methods=["GET"])
def test_success():
    predictions = predict({})
    return render_template(
        "success.html", predictions=predictions, candidatos=CANDIDATOS
    )




@bp.route("/update_quiz", methods=["POST"])
def add_mail():
    if request.method == "POST":
        db_manager.update_quiz(request.form, int(session["answer_id"]))
        return redirect("/")


@bp.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        if session["page"] == len(PREGUNTAS):
            if not validate_captcha(request.form.get("g-recaptcha-response")):
                return (
                    "No pudimos verificar que seas humano.\n"
                    "Beep boop. Hola señor robot."
                )

        session["page"] += 1
        for key, value in request.form.items():
            session[key] = value

        for category in PREGUNTAS:
            for question in category["questions"]:
                if question["id"] not in session:
                    return render_template(
                        "questions.html",
                        num_categories=len(PREGUNTAS),
                        preguntas=[category],
                        respuestas=RESPUESTAS,
                        page=session["page"],
                        recaptcha_site_key=RECAPTCHA_SITE_KEY
                    )

        if validate(session):
            predictions = predict(session)
            answer_id = db_manager.save_response(session)
            session["answer_id"] = answer_id

            return render_template(
                "success.html", predictions=predictions, candidatos=CANDIDATOS
            )
        else:
            # Esto también
            return "Error"

    session.clear()
    session["page"] = 0
    return render_template("main.html")


def validate(form):
    valid_keys = {*QUESTION_KEYS}
    return all(form.get(key, "").isdecimal() for key in valid_keys)
