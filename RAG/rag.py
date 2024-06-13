import sys
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
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
from loader.vectorstore import VectorStore

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
    prompt = ChatPromptTemplate.from_messages([
        ("system", TEMPLATE),
        ("context", "{context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    return prompt

def format_docs(docs):
    context = ""
    metadata = "" # ademas de lesson y subject va a tener la metadata necesaria para devolver el video (url, start, etc)
    for doc in docs:
        context += "Contenido: " + doc.page_content + "\n"
        # subject = SubjectModel()
        # subject = subject.get(doc.metadata['subject_id'])
        #context += "Asignatura: " + subject['name'] + "\n"
        lesson = LessonModel().get(doc.metadata['lesson_id'])
        context += "Clase: " + lesson['name'] + "\n\n"
        metadata += doc.metadata['lesson_id'] + str(doc.metadata['start']) + "\n"
    return context#, metadata

@traceable
def rag(query):
    llm = initialize_llm()

    retriever = initialize_retriever()

    prompt = initialize_prompt()

    print("defini el prompt")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()} # RunnablePassthrough() copies the user’s question. It is a runnable that behaves almost like the identity function, except that it can be configured to add additional keys to the output, if the input is a dict.
        | prompt
        | llm
        | StrOutputParser() # converts any input into a string
    )
    
    print("defini la rag_chain")
    
    demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

    rag_chain_with_history = RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: demo_ephemeral_chat_history_for_chain, # El front deberia pasar un session id (establecer uno al entrar a la pagina, y cada vez que se recarga, limpiar el chat y enviar un session id nuevo). Ver como borrar la historia cada vez que se recibe un session id nuevo
        input_messages_key="question",
        history_messages_key="history",
    )

    print("defini la rag_chain_with_history")

    return rag_chain_with_history.invoke(
        {"question": query},
        {"configurable": {"session_id": "unused"}},
    )#, metadata

if __name__ == "__main__":
    response = rag("Qué es la evolución natural?")
    print(response)
    response2 = rag("Cuál fue mi primera pregunta?")
    print(response2)
