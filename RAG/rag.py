import sys
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langsmith import traceable

# Add parent directory to the sys.path (list of directories where Python is going to search for modules when doing imports)
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from RAG.prompt import TEMPLATE
from loader.vectorstore import VectorStore
from store.data.models.subjects import SubjectModel
from store.data.models.lessons import LessonModel

load_dotenv(override=True)

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = str(os.getenv("LANGCHAIN_API_KEY"))
os.environ["LANGCHAIN_PROJECT"] = "WebIR"

def initialize_llm():
    HUGGINGFACEHUB_API_TOKEN = str(os.getenv("HUGGINGFACEHUB_API_TOKEN"))
    return HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.5,
        huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    )

def initialize_retriever():
    vectorstore = VectorStore()
    retriever = vectorstore.db.as_retriever()
    return retriever

def initialize_prompt():
    template = TEMPLATE # the prompt template takes in context and question as values to be substituted in the prompt
    return ChatPromptTemplate.from_messages(template)

def format_docs(docs):
    context = ""
    for doc in docs:
        context += "Contenido: " + doc.page_content + "\n"
        # subject = SubjectModel()
        # subject_name = subject.get(doc.metadata['subject_id'])
        #context += "Asignatura: " + doc.metadata['lesson_id'] + "\n"
        #lessons = LessonModel()
        #lesson_name = lessons.get(doc.metadata['lesson_id'])
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