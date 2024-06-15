import sys
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langsmith import traceable

# Add parent directory to the sys.path (list of directories where Python is going to search for modules when doing imports)
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from RAG.prompt import PROMPT
from RAG.contextualize_prompt import CONTEXTUALIZE_PROMPT
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

def initialize_retriever(llm):
    vectorstore = VectorStore()
    retriever = vectorstore.db.as_retriever()
    
    # First we define a sub-chain that takes historical messages and the latest user question, and reformulates the question if it makes reference to any information in the historical information.
    # Prompt to contextualize/reformulate the question to include history:
    contextualize_q_system_prompt = CONTEXTUALIZE_PROMPT
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    # MessagesPlaceholder variable under the name "chat_history": pass in a list of Messages to the prompt that will be inserted after the system message and before the human message.
    
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    # create_history_aware_retriever: Creates a chain that takes conversation history and returns documents.
    # Input keys: input and chat_history
    # Output: has the same output schema as a retriever (returns documents)
    # If there is no chat_history, then the input is just passed directly to the retriever.
    # If there is chat_history, then the prompt and LLM will be used to generate the search query. That search query is then passed to the retriever.
    
    return history_aware_retriever

def initialize_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", PROMPT),
        MessagesPlaceholder(variable_name="chat_history"), # Prompt template that assumes variable is already list of messages.
        ("human", "{input}"),
    ])

    return prompt

def format_docs(docs):
    context = ""
    metadata = "" # ademas de lesson y subject va a tener la metadata necesaria para devolver el video (url, start, etc)
    for doc in docs:
        context += "Contenido: " + doc.page_content + "\n"
        lessonId = doc.metadata['lesson_id']
        lesson = LessonModel().get(lessonId, True)
        context += "Asignatura: " + lesson["subject"]['name'] + "\n"
        context += "Clase: " + lesson['name'] + "\n\n"
        metadata += doc.metadata['lesson_id'] + str(doc.metadata['start']) + "\n"
    return context#, metadata

@traceable
def rag(query, chat_history):
    llm = initialize_llm()

    history_aware_retriever = initialize_retriever(llm)

    prompt = initialize_prompt()

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    # create_stuff_documents_chain: Creates a chain for passing a list of Documents (context) to a model.
    # It generates a question_answer_chain.
    # Input keys: context, chat_history, and input.

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    # create_retrieval_chain: Creates retrieval chain that retrieves documents and then passes them on.
    # Applies the history_aware_retriever and question_answer_chain in sequence, retaining intermediate outputs such as the retrieved context for convenience.
    # Input keys: input and chat_history
    # Output: input, chat_history, context, and answer

    return rag_chain.invoke({"input": query, "chat_history": chat_history}) #, metadata

if __name__ == "__main__":
    chat_history = []

    question = "Qué es la evolución natural?"
    ai_msg_1 = rag(question, chat_history)
    chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])
    
    print('\nAnswer to first question: ', ai_msg_1["answer"])
    print('\nchat_history: ', chat_history)

    second_question = "Cuál fue mi primera pregunta?"
    ai_msg_2 = rag(second_question, chat_history)
    chat_history.extend([HumanMessage(content=second_question), ai_msg_2["answer"]])

    print('\nAnswer to second question: ', ai_msg_2["answer"])
    print('\nchat_history: ', chat_history)
