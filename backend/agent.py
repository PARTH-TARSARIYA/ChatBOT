from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
import tempfile
from fastapi import FastAPI, UploadFile, Form, HTTPException, File
import os

load_dotenv()

app = FastAPI(
    title = 'PDF Question Answering API',
    description = 'Ask questions based on uploaded PDF document',
    version = '1.0.0'
)

@app.get('/')
def home():
    return {
        'message' : 'PDF QA is running'
    }

@app.get('/health')
def health():
    return {
        'status' : 'healthy' 
    }




def load_pdf(uploaded_file:UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:

        content = uploaded_file.file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    loader = PyPDFLoader(temp_path)
    pages = loader.load()

    if os.path.exists(temp_path):
        os.remove(temp_path)

    return pages


def pdf_to_text(pdf):
    return "\n".join(page.page_content for page in pdf)


def create_chain():
    model = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0
    )

    prompt = PromptTemplate(
        template="""
        You are an expert at answering questions based only on the PDF context.

        PDF Context:
        {context}

        User Query:
        {query}

        Answer the user's question using only the PDF context.

        If the question cannot be answered from the PDF context, 
        simply write:
        "Your query is out of context!"
        """,
        input_variables=["context", "query"]
    )

    parser = StrOutputParser()

    return prompt | model | parser


def ask_question(chain, pdf_content, user_input):
    return chain.invoke({
        "context": pdf_content,
        "query": user_input
    })


@app.post('/ask')
async def ask(
    file : UploadFile = File(),
    question : str = Form()
):
    if file.content_type != 'application/pdf':
        raise HTTPException(
            status_code = 400,
            detail = 'Upload pdf file only'
        )

    try:
        pdf = load_pdf(file)

        pdf_content = pdf_to_text(pdf)

        chain = create_chain()

        answer = ask_question(chain, pdf_content, question)

        return {
            'question' : question,
            'answer' : answer
        }

    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail = str(e)
        )
    