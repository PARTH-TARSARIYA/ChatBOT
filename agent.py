from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

pdf_loader = PyPDFLoader("D:/parth/Clg PPT/DL/Unit 1 - Types of Gradient Descents.pdf")
pdf = pdf_loader.load()

pdf_content = "\n".join(page.page_content for page in pdf)

user_input = 'what is knowledge representation?'
model = ChatGroq(
    model = 'llama-3.3-70b-versatile'
)

prompt = PromptTemplate(
    template = 'You are best at pdf context answering. \
        Here is the pdf text : {context}. User query is {query}. \
        Answer users question related to this pdf texts only.\
        If you find the question is output this pdf then just simple write\
        "Your query is out of context!"',
    input_variables = ['context', 'query']
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke({'context' : pdf_content, 'query': user_input})

print(result)