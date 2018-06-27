#!/usr/bin/python

import sys
import json
import sqlite3 as sql

db=sql.connect("tails.sqlite")
curs=db.cursor()

#  SYSTEMS schema-version and serial number
# Collect Schema version and serial number
with open("var/jaguar/configs/active/systems.json", "r") as f:
	systems=json.load(f)
version=[x['value'] for x in systems if x['_id']=="schema-version" ][0]
with open("var/jaguar/configs/active/lruprofiles.json", "r") as f:
	lru=json.load(f)
serial=[x['serial'] for x in lru][0]
with open("var/jaguar/configs/active/wowmons.json", "r") as f:
	wowmons=json.load(f)
wow=[x.get('source') for x in wowmons if x.get('_id')=="wow"][0]
curs.execute("insert into systems values (?,?,?)",[serial,version,wow])

#  RADIOS
#
with open("var/jaguar/configs/active/radios.json", "r") as f:
	radios=json.load(f)
for dev,cabin,fbo in [(x['device'],x['cabin'],x['fbo']) for x in radios ]:
	curs.execute("insert into radios values (?,?,?,?)",[serial,dev,cabin,fbo])

#  WIFI APs
#
with open("var/jaguar/configs/active/clients.json", "r") as f:
	clients=json.load(f)
cabin=[x['aps'] for x in clients if x['_id']=="int-cabin" ][0]
aps=[(x['device'],x['ssid'],x['psk']) for x in cabin]
for dev,ssid,psk in aps:
	curs.execute("insert into aps values (?,?,?,?)",[serial,dev,ssid,psk])

#  BEARERS
#
with open("var/jaguar/configs/active/bearers.json", "r") as f:
	bearers=json.load(f)
for bear, ena in [(x['_id'],x['enabled']) for x in bearers ]:
	curs.execute("insert into bearers values (?,?,?)",[serial,bear,ena])

#  429 BUSES
#
with open("var/jaguar/configs/active/a429.json", "r") as f:
	a429s=json.load(f)
arincs=[(x.get('_id'),x.get('parity'),x.get('speed')) for x in a429s if x.get('enabled')]
for aid,parity,speed in arincs:
	curs.execute("insert into a429s values (?,?,?,?)",[serial,aid,parity,speed])
	
#  429 LABELS
#
with open("var/jaguar/casp/config.json", "r") as f:
	casp=json.load(f)
ldict=casp.get('labels',{})
labels=ldict.keys()
for name,lvals in ldict.iteritems():
	conf=lvals.get('config',{})
	curs.execute("insert into labels values (?,?,?,?)",[serial,name,conf.get('label'),conf.get('port')])

#  MAPS
#
with open("var/jaguar/configs/active/movingmaps.json", "r") as f:
	mmaps=json.load(f)
for mlabel,alabel in [ (x.get('_id'),x.get('active_label')) for x in mmaps if x.get('active_label')]:
	curs.execute("insert into maps values (?,?,?)",[serial,mlabel,alabel])

try:
	with open("var/jaguar/configs/active/rcairshows.json", "r") as f:
		rcas=json.load(f)
	rca=rcas[0]
	for k,v in rca.iteritems():
		if v != "NONE" and k != '_id':
			curs.execute("insert into rcairshows values (?,?,?)",[serial,k,v])
except IOError as e:
	print e.strerror,e.filename


#  GPIOS
#
try:
	with open("var/jaguar/configs/active/functions.json", "r") as f:
		funcs=json.load(f)
	for fs in [x for x in funcs if x.get('gpio',False)]:
		curs.execute("insert into functions values (?,?,?)",[serial,fs.get('_id'),fs.get('gpio')])
except IOError as e:
	print e.strerror,e.filename
curs.close()

db.commit()


