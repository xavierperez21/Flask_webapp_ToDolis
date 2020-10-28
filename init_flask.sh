# !/bin/bash
# Programm to initialize flask and its environment variables
# Autor: Luis Xavier Pérez | xavierpm1221@gmail.com | 27 / 10 / 2020

source ./venv/bin/activate

export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development

flask run
