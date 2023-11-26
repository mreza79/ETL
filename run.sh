#!/bin/sh
echo "creating virtual environment"
python3.12 -m venv venv
echo "activating venv"
source venv/bin/activate
echo "installing requirements"
pip3 install -r requirements.txt
echo "running main.py"
python3 main.py