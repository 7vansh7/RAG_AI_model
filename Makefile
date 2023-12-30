run: frontend.py
	sudo streamlit run frontend.py

setup: requirements.txt
	python3 -m venv env
	source env/bin/activate
	pip install -r requirements.txt

commit: 
	git add .
	git commit -m '$(m)'
	git push origin main