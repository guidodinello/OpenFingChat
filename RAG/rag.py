from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_openai import ChatOpenAI
from langsmith import traceable

import constants
from loader.vectorstore import VectorStore
from RAG.contextualize_prompt import CONTEXTUALIZE_PROMPT
from RAG.prompt import PROMPT


def initialize_llm():
    return ChatOpenAI(model="gpt-4o", temperature=0, api_key=constants.OPENAI_API_KEY)
    # HUGGINGFACEHUB_API_TOKEN = str(os.getenv("HUGGINGFACEHUB_API_TOKEN"))
    # return HuggingFaceEndpoint(
    #     repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    #     temperature=0.5,
    #     huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    # )


def initialize_retriever(llm):
    vectorstore = VectorStore()
    retriever = vectorstore.db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 2, "score_threshold": 0.2},
    )

    # First we define a sub-chain that takes historical messages and the latest user question, and reformulates the question if it makes reference to any information in the historical information.
    # Prompt to contextualize/reformulate the question to include history:
    contextualize_q_system_prompt = CONTEXTUALIZE_PROMPT
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(
                "chat_history"
            ),  # Prompt template that assumes variable is already list of messages.
            ("human", "{input}"),
        ]
    )
    # MessagesPlaceholder variable under the name "chat_history": pass in a list of Messages to the prompt that will be inserted after the system message and before the human message.

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    # create_history_aware_retriever: Creates a chain that takes conversation history and returns documents.
    # Input keys: input and chat_history
    # Output: has the same output schema as a retriever (returns documents)
    # If there is no chat_history, then the input is just passed directly to the retriever.
    # If there is chat_history, then the prompt and LLM will be used to generate the search query. That search query is then passed to the retriever.

    return history_aware_retriever


def initialize_prompt():
    # This is a prompt template used to format each individual example.
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    # few_shot_prompt = FewShotChatMessagePromptTemplate(
    #     example_prompt=example_prompt,
    #     examples=EXAMPLES,
    # )

    # Assemble our final prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PROMPT),
            # few_shot_prompt,
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    return prompt


def initialize_document_prompt():
    return PromptTemplate(
        input_variables=["page_content", "subject", "lesson"],
        template="Content: {page_content}\nSubject: {subject}\nLesson: {lesson}",
    )


@traceable
def rag(query, chat_history):
    llm = initialize_llm()

    history_aware_retriever = initialize_retriever(llm)

    prompt = initialize_prompt()

    document_prompt = initialize_document_prompt()

    question_answer_chain = create_stuff_documents_chain(
        llm, prompt, document_prompt=document_prompt
    )
    # create_stuff_documents_chain: Creates a chain for passing a list of Documents (context) to a model.
    # It generates a question_answer_chain.
    # Input keys: context, chat_history, and input.
    # question_answer_chain = custom_stuff_documents_chain(llm, prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    # create_retrieval_chain: Creates retrieval chain that retrieves documents and then passes them on.
    # Applies the history_aware_retriever and question_answer_chain in sequence, retaining intermediate outputs such as the retrieved context for convenience.
    # Input keys: input and chat_history
    # Output: input, chat_history, context, and answer

    return rag_chain.invoke({"input": query, "chat_history": chat_history})


if __name__ == "__main__":
    chat_history = []

    # PREGUNTA DE UN TEMA QUE ESTA EN LAS CLASES, Y DESPUES PREGUNTA QUE TESTEA LA MEMORIA
    """
    question = "Qué es la inducción completa?"
    ai_msg_1 = rag(question, chat_history)
    chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])
    
    print('\nAnswer to first question: ', ai_msg_1["answer"])
    print('\nchat_history: ', chat_history)

    second_question = "Cuál fue mi primera pregunta?"
    ai_msg_2 = rag(second_question, chat_history)
    chat_history.extend([HumanMessage(content=second_question), ai_msg_2["answer"]])

    print('\nAnswer to second question: ', ai_msg_2["answer"])
    print('\nchat_history: ', chat_history)
    """

    # PREGUNTA DE UN TEMA QUE NO ESTA EN LAS CLASES
    """
    question = "¿Cómo funcionan los mecanismos de mutación y reparación del ADN?"
    ai_msg_1 = rag(question, chat_history)  
    print('\nAnswer to first question: ', ai_msg_1["answer"])
    """

    # PREGUNTA QUE TESTEA LA MEMORIA Y REFORMULACION DE LA PREGUNTA
    # """
    question = "Qué es la inducción completa?"
    ai_msg_1 = rag(question, chat_history)
    chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

    print("\nAnswer to first question: ", ai_msg_1["answer"])
    print("\nchat_history: ", chat_history)

    second_question = (
        "Podrías darme un ejemplo que muestre la aplicación de esta técnica?"
    )
    ai_msg_2 = rag(second_question, chat_history)
    chat_history.extend([HumanMessage(content=second_question), ai_msg_2["answer"]])

    print("\nAnswer to second question: ", ai_msg_2["answer"])
    print("\nchat_history: ", chat_history)
    # """

    # PREGUNTA QUE TESTEA CUANDO SE PIDE UN EJEMPLO (que no invente ejemplos)
    """
    question = "Podrías darme un ejemplo de una demostración utilizando inducción completa?"
    ai_msg_1 = rag(question, chat_history)
    chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])
    
    print('\nAnswer to first question: ', ai_msg_1["answer"])
    print('\nchat_history: ', chat_history)
    """
