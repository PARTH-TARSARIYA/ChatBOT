import streamlit as st
import requests

st.set_page_config(page_title = 'PDF Agent')

st.title('PDF QA Bot')

API_URL = 'http://127.0.0.1:8000/ask'

uploaded_pdf = st.file_uploader(
    'Upload a pdf file',
    type = ['pdf']
)

if uploaded_pdf:
    user_input = st.text_input('Ssk a question')

    if st.button('Submit'):
        if not user_input:
            st.warning('Please enter a question')

        else:
            with st.spinner('Processing...'):
                try:
                    files = {
                        'file':(
                            uploaded_pdf.name,
                            uploaded_pdf.getvalue(),
                            'application/pdf'
                        )
                    }

                    data = {
                        'question' : user_input
                    }

                    response = requests.post(
                        API_URL,
                        files = files,
                        data = data
                    )

                    if response.status_code == 200:
                        result = response.json()

                        st.subheader('Answer')
                        st.write(result['answer'])

                    else:
                        st.error(
                            f'backend error : {response['text']}'
                        )

                except requests.exceptions.ConnectionError:
                    st.error(
                        'could not connect to FastAPI backend'
                        'make sure the FastAPI is working'
                    )

                except Exception as e:
                    st.error(
                        f'Error :{str(e)}'
                    )