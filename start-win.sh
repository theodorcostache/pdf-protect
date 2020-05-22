#!/bin/bash

if [ ! -d env ]; then
    python -m virtualenv env
    source env/Scripts/activate
    pip install -r requirements.txt
else
    source env/Scripts/activate
fi

python app/main.py