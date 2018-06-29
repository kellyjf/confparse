#!/usr/bin/env python


from flask import Flask,render_template,url_for
import sqlite3 as sq

db=sq.connect("tails.sqlite")
db.row_factory=sq.Row
curr=db.cursor()

app=Flask(__name__)

@app.route("/tails/<id>")
def tails(id):
	return "Tail {}".format(id)

@app.route("/systems")
def systems():
	ret="<html><table>"
	systems=curr.execute("select version as schema,count(*) as count from systems group by 1 order by 1")	
	systems=systems.fetchall()
	return render_template('out.html',systems=systems)
	
app.run(host="0.0.0.0", port=5555)
