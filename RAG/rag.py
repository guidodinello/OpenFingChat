import sys
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith import traceable

# Add parent directory to the sys.path (list of directories where Python is going to search for modules when doing imports)
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from RAG.prompt import TEMPLATE
from loader.embeddings import Embeddings

load_dotenv(override=True)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_PROJECT"] = "WebIR"

HUGGINGFACEHUB_API_TOKEN = str(os.getenv("HUGGINGFACEHUB_API_TOKEN"))
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

def initialize_llm():
    return HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.5,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )

def initialize_embeddings():
    CACHE_PATH = str(os.getenv("CACHE_PATH"))
    return Embeddings.load(cache_path=CACHE_PATH)

def initialize_retriever():
    embeddings = initialize_embeddings()
    vectorstore = FAISS.load_local("../vector_db_test", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    return retriever

def initialize_prompt():
    template = TEMPLATE # the prompt template takes in context and question as values to be substituted in the prompt
    return PromptTemplate.from_template(template)

def format_docs(docs):
    context = ""
    for doc in docs:
        context += "Contenido: " + doc.page_content + "\n"
        #context += "Asignatura: " + doc.metadata['lesson_id'] + "\n"
        context += "Clase: " + doc.metadata['lesson_id'] + "\n\n"
    print(context)
    return context

@traceable
def rag(query):
    llm = initialize_llm()

    retriever = initialize_retriever()

    prompt = initialize_prompt()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()} # RunnablePassthrough() copies the user’s question. It is a runnable that behaves almost like the identity function, except that it can be configured to add additional keys to the output, if the input is a dict.
        | prompt
        | llm
        | StrOutputParser() # converts any input into a string
    )

    return rag_chain.invoke(query)

if __name__ == "__main__":
    response = rag("Qué es la programación lógica?")
    print(response)