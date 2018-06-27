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


curs.close()

db.commit()


