from app.rag.vector_store import (
    search_documents
)





def retrieve_context(
    query: str
):


    results = search_documents(
        query
    )



    documents = results.get(
        "documents",
        []
    )



    if not documents:


        return "No relevant information found."



    context = "\n\n".join(

        documents[0]

    )



    return context