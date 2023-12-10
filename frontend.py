import streamlit as st
import backend as B


st.title(":rainbow[AI Professor] :pencil: ")

st.write('Upload your document')
with st.form("upload"):
        document = st.file_uploader(label=' ')
        st.form_submit_button('Upload')
if document is not None:
    B.document_to_vector(document)

st.write('Task')
task = st.selectbox('Pick your Task',['-','question-answering','summarisation'])


if task == 'question-answering':
   with st.form("form"):
        st.write('Question')
        question = st.text_input('Write your question here')
        st.form_submit_button('Answer')
        answer = B.ques_to_answer(question)
        st.write(answer)

   




