import chromadb

from chromadb.config import Settings





client = chromadb.PersistentClient(

    path="vector_db/chroma"

)





collection = client.get_or_create_collection(

    name="hobbyfi_knowledge"

)





def add_documents(
    documents: list,
    ids: list
):


    collection.add(

        documents=documents,

        ids=ids

    )





def search_documents(
    query: str,
    limit: int = 3
):


    results = collection.query(

        query_texts=[query],

        n_results=limit

    )


    return results