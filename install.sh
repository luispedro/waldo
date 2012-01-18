#!/bin/sh

cd data/
./update.sh
cd ..
python<scripts/create_tables.py
python<scripts/load_data.py
python setup.py install

