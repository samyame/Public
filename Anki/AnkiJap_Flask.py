from flask import Flask, render_template, request
import pandas as pd
import datetime
from flask_sqlalchemy import SQLAlchemy
from AnkiJapFlaskroot import RanPick, Convert, Question, Check

#cd Documents\GitHub\Perso\Anki
#set FLASK_APP=AnkiJap_Flask.py
#set FLASK_ENV=development

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ankiscore.db'
db = SQLAlchemy(app)

class High(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    scor = db.Column(db.Integer())
    coun = db.Column(db.Integer())
    ratio = db.Column(db.Float())
    dat = db.Column(db.String())
    mode = db.Column(db.String())

class Difficult(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    en = db.Column(db.String())
    jp = db.Column(db.String())
    kotoba = db.Column(db.String())

GramVoc = 'A'
mode = 'A'
mode2 = 'A'
choice = 'A'
answer = 'A'
daf = pd.DataFrame()
outpu = 'A'
inpu = 'A'
query = 'A'
score = 0
count = 0
propositions = []
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


#Flask Application
@app.route('/', methods=['GET'])
def start():
    global score
    global count
    score = 0
    count = 0
    return render_template('Grammar.html')



@app.route('/test', methods=['GET','POST'])
def test():
    global GramVoc
    global mode
    global mode2
    global answer
    global daf
    global inpu
    global next
    global propositions
    if request.method == 'POST':
        mode = request.form.get('lang')
        GramVoc = request.form.get('text')
        mode2 = request.form.get('diff')
    answer,prop,daf = RanPick(mode2,GramVoc)
    propositions = Convert(mode,prop,daf)
    proplen = len(propositions)
    question,inpu = Question(mode,answer,daf)
    return render_template('test.html', GramVoc=GramVoc, mode=mode,mode2=mode2, propositions=propositions, proplen=proplen, question=question, choice=choice)

@app.route('/result', methods=['GET','POST'])
def result():
    global choice
    global answer
    global outpu
    global count
    global score
    if request.method == 'POST':
        choice = request.form.get('submit_button')
        result,outpu,phonetic,correct,count,score,en,jp,koto = Check(mode,choice,answer,daf,count,score,propositions)
        choicetxt=propositions[int(choice)]
        if result == False:
            err = Difficult(en=en,jp=jp,kotoba=koto)
            db.session.add(err)
            db.session.commit()
    return render_template('Result.html', choicetxt=choicetxt, result=result, score=score, phonetic=phonetic,correct=correct, count=count)

@app.route('/finish', methods = ['GET','POST'])
def finish():
    global GramVoc
    global mode
    global mode2
    global score
    global count
    global date
    global query
    mod = (GramVoc+' '+mode+' '+mode2)
    rati = round((score/count)*100,2) if count != 0 else 0
    score1 = High(scor = score, coun = count,ratio = rati, dat = date, mode = mod )
    db.session.add(score1)
    db.session.commit()
    query = High.query.filter(High.coun != 0 and High.scor != 0).order_by(High.ratio.desc()).order_by(High.coun.desc()).limit(5)
    return render_template('Finish.html', query = query,GramVoc=GramVoc,mode=mode,mode2=mode2)