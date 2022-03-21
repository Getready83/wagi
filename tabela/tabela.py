from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

tabela = Flask(__name__)
tabela.config["SQLALCHEMI_DATABASE_URI"] = "sqlite:///test1.db"
db = SQLAlchemy(tabela)


class Adda(db.Model):
    number = db.Column(db.String(8), primary_key=True)
    segment = db.Column(db.Integer)
    surface = db.Column(db.Integer)
    habitants = db.Column(db.Integer)

db.create_all()

the_getler = Adda(
    number=1,
    segment=2,
    surface=55,
    habitants=5
)
db.session.add(the_getler)
db.session.commit()

