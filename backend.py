import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

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
    # loader = PyPDFLoader(file)
    # data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(data)
    docsearch = Pinecone.from_texts([t.page_content for t in texts], hf, index_name='document-reader')
    return docsearch


def ques_to_answer(question):
    query = question
    docsearch = Pinecone.from_existing_index('document-reader',hf)
    docs =docsearch.similarity_search(query=query)


    llama = LlamaAPI(os.getenv('LLAMA_API_KEY'))
    model = ChatLlamaAPI(client=llama)

    chain = load_qa_chain(model, chain_type="stuff")
    
    answer = chain.run(input_documents=docs, question=query)
    return answer


# working on the summarisation part of the app