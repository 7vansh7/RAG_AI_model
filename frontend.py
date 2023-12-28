import streamlit as st
import backend as B


st.set_page_config(page_title="AI Analyst")
st.title(":rainbow[AI Analyst] :bar_chart: ")
st.write('Task')
task = st.selectbox('Pick your Task',['-','question-answering','summarization','pdf-image-analysis','chat'])
if task == 'pdf-image-analysis':
    model = 'gemini-pro-vision'
    st.write('Model: Gemini-pro-vision')
else:
    model = st.selectbox('Select the model',['gemini-ultra','gemini-pro','llama2','chatgpt'])
model = B.model_used(model)
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
        if st.form_submit_button('Answer',type='primary'):
            with st.spinner('💬...'):
                answer = B.ques_to_answer(llm=model,question=question)
                st.write(answer)

if task == 'summarization' :
        
     
        st.write('Upload your document')
        with st.form("upload"):
            document = st.file_uploader(label=' ')
            btn =st.form_submit_button('Upload')
        if document is not None:
            with st.form('summarize'):   
                if st.form_submit_button('Summarize the text',type='primary'):
                    with st.spinner('Converting...'):
                        summary = B.summarize(llm=model, document=document)
                        st.write(summary)
                    st.success('Done!!', icon="✅")

if task == 'pdf-image-analysis' :
     st.write('Upload your document')
     with st.form("upload"):
        document = st.file_uploader(label=' ')
        btn =st.form_submit_button('Upload')

     if document is not None:
        with st.form('pdf-image-analysis'):
            if st.form_submit_button('Analyze',type='primary'):
                with st.spinner('Analyzing...'):
                    summary,images=B.image_analysis(image_doc=document)
                    for img in images:
                        st.image(img)
                    st.write(summary)
                st.success('Done!!', icon="✅")

if task == 'chat':

    with st.form("form"):
        st.write('Question')
        question = st.text_input('Write your question here')
        if st.form_submit_button('Answer',type='primary'):
            with st.spinner('💬...'):
                answer = B.chat(llm=model,question=question)
                st.write(answer)