from .vectorstore import VectorStore

if __name__ == "__main__":
    db = VectorStore()
    docs = db.db.similarity_search("Que son las combinaciones?")
    print(docs)
