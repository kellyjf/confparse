#!/usr/bin/env python


from flask import Flask,render_template,url_for,g
import sqlite3 as sq

def get_cursor():
	if 'db' not in g:
		g.db=sq.connect("tails.sqlite")
		g.db.row_factory=sq.Row
		print "New Connection"

	curr=g.db.cursor()
	return curr

app=Flask(__name__)

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
	
app.run(host="0.0.0.0", port=5555)
