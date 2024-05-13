from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import json
import random

app = Flask(__name__, static_folder="C:\\Users\\abein\\Desktop\\saod coursework theory\\templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "NoneOfYourBusiness"
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    answers = db.Column(db.String())
    type = db.Column(db.Integer)
    right_answer = db.Column(db.Integer)

    def __init__(self, id, text, answers, right_answer, type=0):
        self.id = id
        self.text = text
        self.answers = json.dumps(answers, ensure_ascii=False)
        self.type = type
        self.right_answer = right_answer
       

questions_easy = []
questions_medium = []
questions_hard = []


def change_into_tuple(questions):
    return [(q.id, q.text, json.loads(q.answers), q.right_answer, q.type) for q in questions]


with app.app_context():
    questions_easy = Question.query.filter(Question.type == 0).all()
    if len(questions_easy):
        questions_easy = change_into_tuple(questions_easy)
    
    questions_medium = Question.query.filter(Question.type == 1).all()
    if len(questions_medium):
        questions_medium = change_into_tuple(questions_medium)
    
    questions_hard = Question.query.filter(Question.type == 2).all()
    if len(questions_hard):
        questions_hard = change_into_tuple(questions_hard)


@app.route('/result', methods=['POST'])
def results():
    if request.method == "POST":
        right_answers = 0
        answers = list(request.form.to_dict().values())
        q = []
        for i in range(len(answers)):
            if session["type"] == 0:
                q = questions_easy
                right_answers += int(answers[i]) == questions_easy[i][3]
            if session["type"] == 1:
                q = questions_medium
                right_answers += int(answers[i]) == questions_medium[i][3]
            if session["type"] == 2:
                q = questions_hard
                right_answers += int(answers[i]) == questions_hard[i][3]
        return render_template('result.html', correct_answers=right_answers, total_questions=len(answers), questions=q)
    

@app.route('/')
def basic_page():
    return render_template('basic.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/choose', methods=["GET", "POST"])
def choose():
    session["name"] = request.form["name"]
    return render_template('choose_page.html', name=request.form["name"])


@app.route('/theory')
def theory():
    return render_template('theory.html')


@app.route('/test_easy', methods=['POST', 'GET'])
def test_easy():
    if request.method == 'POST':
        session["type"] = 0
        random.shuffle(questions_easy)
        return render_template('test.html', questions=questions_easy, name=session["name"])
    return render_template('index.html')


@app.route('/test_medium', methods=['POST', 'GET'])
def test_medium():
    if request.method == 'POST':
        session["type"] = 1
        random.shuffle(questions_medium)
        return render_template('test.html', questions=questions_medium, name=session["name"])
    return render_template('index.html')


@app.route('/test_hard', methods=['POST', 'GET'])
def test_hard():
    if request.method == 'POST':
        session["type"] = 2
        random.shuffle(questions_hard)
        return render_template('test.html', questions=questions_hard, name=session["name"])
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)