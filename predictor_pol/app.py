from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/respuestas',methods=['POST'])
def answers():
    return render_template('main.html')
