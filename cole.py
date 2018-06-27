#!/usr/bin/python

import sys
import json
import sqlite3 as sql

with open("var/jaguar/configs/active/systems.json", "r") as f:
	systems=json.load(f)
with open("var/jaguar/configs/active/lruprofiles.json", "r") as f:
	lru=json.load(f)
with open("var/jaguar/configs/active/bearers.json", "r") as f:
	bearers=json.load(f)
with open("var/jaguar/configs/active/clients.json", "r") as f:
	clients=json.load(f)
with open("var/jaguar/configs/active/radios.json", "r") as f:
	radios=json.load(f)
with open("var/jaguar/configs/active/wowmons.json", "r") as f:
	wowmons=json.load(f)


wow=[x.get('source') for x in wowmons if x.get('_id')=="wow"][0]

serial=[x['serial'] for x in lru][0]
version=[x['value'] for x in systems if x['_id']=="schema-version" ][0]
b=[(x['_id'],x['enabled']) for x in bearers ]
r=[(x['device'],x['cabin'],x['fbo']) for x in radios ]
cabin=[x['aps'] for x in clients if x['_id']=="int-cabin" ][0]
aps=[(x['device'],x['ssid'],x['psk']) for x in cabin]


db=sql.connect("tails.sqlite")
curs=db.cursor()

curs.execute("insert into systems values (?,?,?)",[serial,version,wow])

for bear, ena in b:
	curs.execute("insert into bearers values (?,?,?)",[serial,bear,ena])

for dev,cabin,fbo in r:
	curs.execute("insert into radios values (?,?,?,?)",[serial,dev,cabin,fbo])

for dev,ssid,psk in aps:
	curs.execute("insert into aps values (?,?,?,?)",[serial,dev,ssid,psk])


with open("var/jaguar/configs/active/functions.json", "r") as f:
	funcs=json.load(f)
for fs in [x for x in funcs if x.get('gpio',False)]:
	curs.execute("insert into functions values (?,?,?)",[serial,fs.get('_id'),fs.get('gpio')])

with open("var/jaguar/configs/active/a429.json", "r") as f:
	a429s=json.load(f)
arincs=[(x.get('_id'),x.get('parity'),x.get('speed')) for x in a429s if x.get('enabled')]
for aid,parity,speed in arincs:
	curs.execute("insert into a429s values (?,?,?,?)",[serial,aid,parity,speed])
	
with open("var/jaguar/configs/active/a429.json", "r") as f:
	a429s=json.load(f)
arincs=[(x.get('_id'),x.get('parity'),x.get('speed')) for x in a429s if x.get('enabled')]
for aid,parity,speed in arincs:
	curs.execute("insert into a429s values (?,?,?,?)",[serial,aid,parity,speed])
	
with open("var/jaguar/casp/config.json", "r") as f:
	casp=json.load(f)
ldict=casp.get('labels',{})
labels=ldict.keys()
for name,lvals in ldict.iteritems():
	conf=lvals.get('config',{})
	curs.execute("insert into labels values (?,?,?,?)",[serial,name,conf.get('label'),conf.get('port')])

with open("var/jaguar/configs/active/movingmaps.json", "r") as f:
	mmaps=json.load(f)
for mlabel,alabel in [ (x.get('_id'),x.get('active_label')) for x in mmaps if x.get('active_label')]:
	curs.execute("insert into maps values (?,?,?)",[serial,mlabel,alabel])

with open("var/jaguar/configs/active/rcairshows.json", "r") as f:
	rcas=json.load(f)
rca=rcas[0]
for k,v in rca.iteritems():
	if v != "NONE" and k != '_id':
		curs.execute("insert into rcairshows values (?,?,?)",[serial,k,v])


curs.close()

db.commit()


