***This is a RAG app that is powered by a generative AI(Llama in this case)***

METHOD 1 (using the script)

1. chmod +x install.sh
2. bash install.sh
3. streamlit run frontend.py


METHOD 2 (entering all the commands manually)

1. git clone https://github.com/7vansh7/education_LLM.git
2. make a .env file and add your api keys
3. python3 venv env
4. source ./env/bin/activate
5. python3 -m requirements.txt
6. streamlit run frontend.py

Name of the .env varaibles - 
LLAMA_API_KEY(for the llama key)
PINECONE_KEY(for the pinecone key)