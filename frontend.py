import streamlit as st
import backend as B


st.set_page_config(page_title="AI Analyst",layout='wide',page_icon=':computer:')
c1, c2 = st.columns((3, 1))
c1.title(":rainbow[AI Analyst] :bar_chart: ")
c1.write('Task')
task = c1.selectbox('Pick your Task',['-','question-answering','summarization','pdf-image-analysis','chat'])
if task == 'pdf-image-analysis':
    model = 'gemini-pro-vision'
    c1.write('Model: Gemini-pro-vision')
else:
    model = c1.selectbox('Select the model',['gemini-pro'])
c1.write('More :blue[MODELS] to be added soon!!')
model = B.model_used(model)

c1.link_button('**CODE** here :computer:',url='https://gitpod.new/',type="primary")
c1.divider()



if task == 'question-answering':
   
    c1.write('Upload your document')
    document = c1.file_uploader(label=' ',type='pdf')
    if c1.button('Upload',type='primary'):
        if document is not None:
            B.document_to_vector(document)

        c1.write('Question')
        question = c1.text_input('Write your question here')
        if c1.button('Answer',type='primary'):
            with st.spinner('💬...'):
                answer = B.ques_to_answer(llm=model,question=question)
                c1.write(answer)
    # c1.write('Please delete your data after using the app')
    # with c1.form('delete vector-data'):
    #     if c1.form_submit_button('Delete Data'):
    #         ans = B.delete_index_data()
    #         if ans == True:
    #             c1.success('Data deleted successfully!')

if task == 'summarization' :
        
     
        c1.write('Upload your document')
        document = c1.file_uploader(label=' ',type='pdf')
        btn =c1.button('Upload',type='primary')
        if document is not None:  
                c1.write('It could take a few minutes')
                if c1.button('Summarize the text',type='primary'):
                    with st.spinner('Converting...'):
                        summary = B.summarize(llm=model, document=document)
                        c1.write(summary)
                    c1.success('Done!!', icon="✅")

if task == 'pdf-image-analysis' :
     c1.write('Upload your document')
     document = c1.file_uploader(label=' ',type='pdf')
     btn =c1.button('Upload',type='primary')

     if document is not None:
            if c1.button('Analyze',type='primary'):
                with st.spinner('Analyzing...'):
                    summary,images=B.image_analysis(image_doc=document)
                    for img in images:
                        c1.image(img)
                    c1.write(summary)
                c1.success('Done!!', icon="✅")

if task == 'chat':

    # with c1.form("form"):
        c1.write('Question')
        question = c1.text_input('Write your question here')
        if c1.button('Answer',type='primary'):
            with st.spinner('💬...'):
                answer = B.chat(llm=model,question=question)
                c1.write(answer)



string = ""
a = c2.text_area(label='**NOTES**',placeholder='Write here',height=400)
string += a
c2.download_button(label='Download Notes',file_name='notes.txt',data=string)
# add some error handling in the string and download button