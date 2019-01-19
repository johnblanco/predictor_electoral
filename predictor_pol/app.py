from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/answers',methods=['POST'])
def answers():
    education = request.form['education']
    inflation = request.form['inflation']

    print(education)
    print(inflation)

    #aca llamamos al modelo de machine learning con las respuestas y calculamos el candidato


    return render_template('main.html')


