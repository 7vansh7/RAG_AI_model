import streamlit as st
import backend as B


st.set_page_config(page_title="AI Analyst",layout='wide',page_icon=':computer:')
c1, c2 = st.columns((3, 1))
c1.title(":rainbow[AI Analyst] :bar_chart: ")
c1.write('Task')
task = c1.selectbox('Pick your Task',['-','quec1ion-answering','summarization','pdf-image-analysis','chat'])
if task == 'pdf-image-analysis':
    model = 'gemini-pro-vision'
    c1.write('Model: Gemini-pro-vision')
else:
    model = c1.selectbox('Select the model',['gemini-pro'])
c1.write('More :blue[MODELS] to be added soon!!')
model = B.model_used(model)
if task == 'quec1ion-answering':
   
    c1.write('Upload your document')
    with c1.form("upload"):
        document = c1.file_uploader(label=' ')
        if c1.form_submit_button('Upload'):
            if document is not None:
                B.document_to_vector(document)

    with c1.form("form"):
        c1.write('Quec1ion')
        quec1ion = c1.text_input('Write your quec1ion here')
        if c1.form_submit_button('Answer',type='primary'):
            with st.spinner('💬...'):
                answer = B.ques_to_answer(llm=model,quec1ion=quec1ion)
                c1.write(answer)
    # c1.write('Please delete your data after using the app')
    # with c1.form('delete vector-data'):
    #     if c1.form_submit_button('Delete Data'):
    #         ans = B.delete_index_data()
    #         if ans == True:
    #             c1.success('Data deleted successfully!')


c1.write(' Write your :blue[**CODE**] here')
c1.link_button('GO',url='https://gitpod.new/',type="primary")

if task == 'summarization' :
        
     
        c1.write('Upload your document')
        with c1.form("upload"):
            document = c1.file_uploader(label=' ')
            btn =c1.form_submit_button('Upload')
        if document is not None:
            with c1.form('summarize'):   
                c1.write('It could take a few minutes')
                if c1.form_submit_button('Summarize the text',type='primary'):
                    with st.spinner('Converting...'):
                        summary = B.summarize(llm=model, document=document)
                        c1.write(summary)
                    c1.success('Done!!', icon="✅")

if task == 'pdf-image-analysis' :
     c1.write('Upload your document')
     with c1.form("upload"):
        document = c1.file_uploader(label=' ')
        btn =c1.form_submit_button('Upload')

     if document is not None:
        with c1.form('pdf-image-analysis'):
            if c1.form_submit_button('Analyze',type='primary'):
                with st.spinner('Analyzing...'):
                    summary,images=B.image_analysis(image_doc=document)
                    for img in images:
                        c1.image(img)
                    c1.write(summary)
                c1.success('Done!!', icon="✅")

if task == 'chat':

    with c1.form("form"):
        c1.write('Quec1ion')
        quec1ion = c1.text_input('Write your quec1ion here')
        if c1.form_submit_button('Answer',type='primary'):
            with st.spinner('💬...'):
                answer = B.chat(llm=model,quec1ion=quec1ion)
                c1.write(answer)



string = ""
a = c2.text_area(label='**NOTES**',placeholder='Write here',height=400)
string += a
c2.download_button(label='Download Notes',file_name='notes.txt',data=string)
