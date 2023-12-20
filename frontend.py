import streamlit as st
import backend as B


st.title(":rainbow[AI Professor] :pencil: ")

st.write('Task')
task = st.selectbox('Pick your Task',['-','question-answering','summarization'])

model = st.selectbox('Select the model',['llama2','chatgpt'])

if task == 'question-answering':
   
    st.write('Upload your document')
    with st.form("upload"):
        document = st.file_uploader(label=' ')
        if st.form_submit_button('Upload'):
            if document is not None:
                B.document_to_vector(document)

    with st.form("form"):
        st.write('Question')
        question = st.text_input('Write your question here')
        if st.form_submit_button('Answer'):
            answer = B.ques_to_answer(question)
            st.write(answer)

if task == 'summarization' :
        
     
        st.write('Upload your document')
        with st.form("upload"):
            document = st.file_uploader(label=' ')
            btn =st.form_submit_button('Upload')
        if document is not None:
            with st.form('summarize'):   
                if st.form_submit_button('Summarize the text'):
                    with st.spinner('Converting...'):
                        summary = B.summarize(document=document)
                        st.write(summary)
                    st.success('Done!!', icon="✅")



