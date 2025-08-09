#Backend Project Setup
#Requirments
Python 3.13.3
pip
virtual environment

#Venv setup
python -m venv venv
source venv/bin/activate  #Linux/Mac
venv\Scripts\activate     #Windows

#Library setup
pip install -r requirements.txt

#Start
fastapi dev main.py
