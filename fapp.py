#!/usr/bin/env python



from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class ExForm(FlaskForm):
	name=StringField('What is your name?',
		validators=[DataRequired()])
	submit=SubmitField('Submit')

from flask import Flask,render_template,url_for,g

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///alchem.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy(app)

app.config['SECRET_KEY']="JFK"
from flask_bootstrap import Bootstrap
bs=Bootstrap(app)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	def __repr__(self):
		return "<Role %r>"%(name)

db.create_all()

@app.route("/role", methods=['GET','POST'])
def role():
	exf=ExForm()
	return render_template('wtf.html',form=exf)

@app.route("/tails/<id>")
def tails(id):
	return "Tail {}".format(id)

@app.route("/system/<id>")
def system(id):
	curr=get_cursor()
	systems=curr.execute("select * from systems where version=? order by serial",[id])	
	systems=systems.fetchall()
	curr.close()
	return render_template('versions.html',systems=systems)

@app.route("/systems")
def systems():
	curr=get_cursor()
	systems=curr.execute("select version as schema,count(*) as count from systems group by 1 order by 1")	
	systems=systems.fetchall()
	curr.close()
	return render_template('out.html',systems=systems)
	
app.run(host="0.0.0.0", port=5555, debug=True)
