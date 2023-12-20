import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
import os
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
from langchain.memory import ConversationBufferMemory

# Change the vectorbase from piencone to ChromaDB


load_dotenv()
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
api_key = os.getenv("PINECONE_KEY")
hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
pinecone.init(      
        api_key=api_key,      
        environment='gcp-starter'      
    )

def document_to_vector(document):

    file = document
    bytes_data = file.read()
    with NamedTemporaryFile(delete=False) as tmp:  
        tmp.write(bytes_data)                      
        data = PyPDFLoader(tmp.name).load()        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(data)
    docs = Pinecone.from_texts([t.page_content for t in texts], hf, index_name='document-reader')
    return docs


def ques_to_answer(question):
    query = question
    docsearch = Pinecone.from_existing_index('document-reader',hf)
    docs =docsearch.similarity_search(query=query)


    llama = LlamaAPI(os.getenv('LLAMA_API_KEY'))
    model = ChatLlamaAPI(client=llama)

    chain = load_qa_chain(model, chain_type="stuff")
    
    answer = chain.run(input_documents=docs, question=query)
    return answer

def summarize(document):

    llama = LlamaAPI(os.getenv('LLAMA_API_KEY'))
    model = ChatLlamaAPI(client=llama)
    txt_file = open('docs/file1.txt','r+')

    file = document
    bytes_data = file.read()
    with NamedTemporaryFile(delete=False) as tmp:  
        tmp.write(bytes_data)                      
        data = PyPDFLoader(tmp.name)       
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400,separators=['\n','\n\n'])    
    texts = data.load_and_split(text_splitter=text_splitter)
    prompt = """
    Write a summary with at least 10 points or as many points as you could of the following text delimited by triple backquotes.
    Return your response in bullet points which covers the key points of the following text which is a collection of summaries.
    ```{text}```
    BULLET POINT SUMMARY:
    """
    prompt = PromptTemplate.from_template(prompt)
    x,y = 0,9
    for _ in range(int(len(texts)/9)):
        prompt2 = """
        Write a long summary for the following texts     
        {text}
        """
        prompt = PromptTemplate.from_template(prompt)
        chain = load_summarize_chain(model,chain_type='refine')
        summary = chain.run(input_documents=texts[x:y],prompt=prompt2)
        txt_file.write(summary + '\n')
        x += 9
        y += 9

    final_docs = TextLoader('docs/file1.txt').load_and_split(text_splitter=text_splitter)

    chain = load_summarize_chain(model,chain_type='map_reduce',map_reduce_prompt=prompt)
    summary = chain.run(input_documents=final_docs)
    return summary

# the flow of the summarizer is -->
# 1. Takes in the pdf
# 2. Converts it into chunks
# 3. summarizes all the chunks and adds them to a variable or a seperate text file
# 4. Takes in all the summaries and then makes a combined summary from them all 
# 5. Spits the combined summary