#!/bin/bash

sqlite3 tails.sqlite < cole.sql

for file in *gz; do
	echo "===============  $file ================="
	rm -rf var
	tar xf $file
	./cole.py
	rm -rf var
done

