#!/usr/bin/env bash

datadir=$PWD/data

python setup.py install
mkdir -p $datadir
./bin/update-waldo --datadir $datadir --database waldo.sqlite3

