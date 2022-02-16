from AnkiJap_Flask import db

#define columns
def CreateDB():
    class Item(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        en = db.Column(db.String())
        jp = db.Column(db.String())
        kotoba = db.Column(db.String())
    
def DFtoDB():
    for i in df1:
        globals()['df%s' % str(i[:2])]
    for i in range(len(dfen)):
        globals()['item%s' % str(i)] = Item(en=dfen[i],jp=dfjp[i],kotoba=dfko[i])
        db.session.add(globals()['item%s' % str(i)])


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

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    en = db.Column(db.String())
    jp = db.Column(db.String())
    kotoba = db.Column(db.String())


db.create_all()
        
