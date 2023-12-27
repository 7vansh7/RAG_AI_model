run: frontend.py
	sudo streamlit run frontend.py

setup: requirements.txt
	python3 -m venv env
	source env/bin/activate
	pip install -r requirements.txt