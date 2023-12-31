import pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from pypdf import PdfReader
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader,TextLoader,MathpixPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from llamaapi import LlamaAPI
from langchain_experimental.llms import ChatLlamaAPI
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.summarize import load_summarize_chain
import os
from io import BytesIO
import PIL.Image
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
import google.generativeai as genai


# Change the vectorbase from piencone to ChromaDB
load_dotenv()
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  }
]
def model_used(model_name):
    if model_name == 'gemini-pro':
        llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key=os.getenv('GOOGLE_API_KEY')
        ,convert_system_message_to_human=True,safety_settings=safety_settings)
    elif model_name == 'gemini-ultra':
        llm = ChatGoogleGenerativeAI(model="gemini-ultra",google_api_key=os.getenv('GOOGLE_API_KEY')
        ,convert_system_message_to_human=True,safety_settings=safety_settings)
    elif model_name == 'llama2':
        llama = LlamaAPI(os.getenv('LLAMA_API_KEY'))
        llm = ChatLlamaAPI(client=llama)
    elif model_name == 'chatgpt':
        llm = None
    elif model_name == 'gemini-pro-vision':
        llm=None
    return llm

llm2 = GoogleGenerativeAI(model="gemini-pro",google_api_key=os.getenv('GOOGLE_API_KEY')
,convert_system_message_to_human=True)
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
index = pinecone.Index("document-reader")
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


def ques_to_answer(llm,question):
    try:
        query = question 
        prompt = f'''You are a helpful and informative bot that answers questions using text from the reference passage included below. 
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. 
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and 
    strike a friendly and converstional tone.
    QUESTION:{query}'''
        docsearch = Pinecone.from_existing_index('document-reader',hf)
        docs =docsearch.similarity_search(query=query)

        chain = load_qa_chain(llm, chain_type="refine")
        
        answer = chain.run(input_documents=docs, question=prompt)
        return answer
    except Exception as e:
        print(e)
        return "Please try again!!"
def summarize(llm,document):
    try:
        txt_file = open('docs/file1.txt','w')

        file = document
        bytes_data = file.read()
        with NamedTemporaryFile(delete=False) as tmp:  
            tmp.write(bytes_data)                      
            data = PyPDFLoader(tmp.name)       
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200,separators=['\n','\n\n'])    
        texts = data.load_and_split(text_splitter=text_splitter)
        print(len(texts))
        if len(texts) % 2 != 0:
            texts = texts[:len(texts)-1]
        print(len(texts))
        prompt = """ Write a summary using all the summaries provided to you and make sure of the 
        followig --
        * Make sure the word length is between 1000 to 3000
        * After giving the summary also give a seperate key points from the context and also expalin every key point vigourously
        * After the above two also give information headers or headings that define the main parts of the book
        * please don't give any kind of finish_reason errors
        * Don't give recitation error
        ```{text}```
        """
        prompt = PromptTemplate(template=prompt,input_variables=['text'])

        # This loop finds the number to be used for the next for loop
        for z in range(5,10):
            if len(texts) % z == 0:
                number = z
        print(number)
        iterations_number = number 
        number = number
        x = 0
        y = number
        iterations = int(len(texts)/iterations_number)
        print(f'number:{number}')
        print(f'iterations:{iterations}')
        for _ in range(iterations):
            print(f'iteration number:{_}')
            print(f'slice:{x,y}')
            prompt2 = """
            Write a long summary for the following texts with at least 100 words each
            Don't give RECITATION error, ALLOW RECITATION
            please don't give any kind of finish_reason errors
            {text}
            """
            prompt2 = PromptTemplate(template=prompt2,input_variables=['text'])
            chain = load_summarize_chain(llm,chain_type='refine',refine_prompt=prompt2,verbose=False)
            summary = chain.run(input_documents=texts[x:y])
            txt_file.write(summary + '\n')
            x += number
            y += number
        txt_file.close()
        text_splitter_2 = RecursiveCharacterTextSplitter()
        final_docs = TextLoader('docs/file1.txt').load_and_split(text_splitter=text_splitter_2)

        chain_final = load_summarize_chain(llm,chain_type='map_reduce',map_prompt=prompt,combine_prompt=prompt,verbose=True)
        summary_final = chain_final.run(input_documents=final_docs)
        # os.remove('/Users/vanshaggarwal/Documents/quine_quest4/app/docs/file1.txt')
        return summary_final    
    except Exception as e:
        print(e)
        return "Please try again!!,if already tried twice then PDF is not compatible for the model "

# the flow of the summarizer is -->
# 1. Takes in the pdf
# 2. Converts it into chunks
# 3. summarizes all the chunks and adds them to a variable or a seperate text file
# 4. Takes in all the summaries and then makes a combined summary from them all 
# 5. Spits the combined summary

def image_analysis(image_doc):
    try:
        images_dic = {}
        images_pil_array = []
        content = []
        file = image_doc
        bytes_data = file.read()
        with NamedTemporaryFile(delete=False) as tmp:  
            tmp.write(bytes_data)                      
            reader = PdfReader(tmp.name)
        for page in reader.pages:
            for index,image in enumerate(page.images):
                images_dic[index] = image
        model = genai.GenerativeModel('gemini-pro-vision')
        for key,value in images_dic.items():
            image_data = BytesIO(value.data)
            # mg = img.name
            # img = PIL.Image.open(img)
            image = PIL.Image.open(image_data)
            images_pil_array.append(image)
            res=model.generate_content(["what can you infer from the image",image])
            content.append(res.text)
        
        return content,images_pil_array
    except:
        return "Please try again"
    

def chat(llm,question):
    try:
        query = question
        answer=llm.invoke(query)
        return f'{answer.content}'
    except Exception as e:
        print(e)
        return "Please ask again"


# def delete_index_data():

#     print(index.delete(delete_all=True))
    