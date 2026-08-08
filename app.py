import streamlit as st
from agent import load_pdf, pdf_to_text, create_chain, ask_question

st.set_page_config(page_title = 'PDF Agent')

st.title('PDF QA Bot')

uploaded_pdf = st.file_uploader('Upload a pdf file', type = ['pdf'])

if uploaded_pdf:
    pdf = load_pdf(uploaded_pdf)

    pdf_content = pdf_to_text(pdf)

    chain = create_chain()

    user_input = st.text_input('Ask a question')

    if user_input:
        if st.button('submit'):
            result = ask_question(chain, pdf_content, user_input)

            st.write(result)
