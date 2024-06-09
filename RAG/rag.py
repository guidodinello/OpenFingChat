from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv(override=True)
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1",
    max_length = 128,
    temperature = 0.5,
    huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN,
)

embeddings = HuggingFaceEmbeddings()
vectorstore = FAISS.load_local("faiss_index", embeddings)
retriever = vectorstore.as_retriever()

template = """You are an intelligent assistant designed to help students find relevant information from university lecture transcriptions stored in a vector database. 
Your response will vary depending on whether you are provided with pieces of retrieved context or not:

1. If relevant chunks are provided:
   - Provide the user with the start minute of the lecture where the topic is discussed.
   - Include the name of the lecture and the subject, that is part of the metadata.
   - Offer a brief summary of the information found in the chunks.
2. If no relevant chunks are provided:
   - Inform the user that there are no lectures in the database that discuss the topic of their question.
   - Provide an answer to the question based on your own knowledge, clearly stating that this information is not from the database.

### Examples

**User Query:** "Can you explain the theory of relativity?"

**Response if relevant chunks are found:**
"In the lecture **Theory of Relativity - Introduction**, from the subject **Physics**, you can find a response to your question starting at minute 15. In this lecture, the basics of the theory of relativity are covered, including the concepts of time dilation and length contraction. It explains how these principles were developed by Albert Einstein and their implications in modern physics."

**Response if no relevant chunks are found:**
"I'm sorry, there are no lectures in the database that discuss the theory of relativity. Based on my own knowledge, the theory of relativity is a fundamental theory in physics developed by Albert Einstein. It includes the special theory of relativity and the general theory of relativity, which describe the laws of physics in the presence of gravitational fields and high velocities."

### Instructions

Please use the following pieces of retrieved context to answer the question, adhering to the outlined format.

Question: {question} 

Context: {context} 

Answer:
"""
# the prompt template takes in context and question as values to be substituted in the prompt

prompt = PromptTemplate.from_template(template) 

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()} # RunnablePassthrough() copies the user’s question. It is a runnable that behaves almost like the identity function, except that it can be configured to add additional keys to the output, if the input is a dict.
    | prompt
    | llm
    | StrOutputParser() # converts any input into a string
)