#!/bin/bash

git clone https://github.com/7vansh7/education_LLM.git
python3 venv env
source ./env/bin/activate
python3 -m requirements.txt
