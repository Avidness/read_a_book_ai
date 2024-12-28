from openai import OpenAI
import pandas as pd
import chromadb

client = OpenAI()

def generate_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def store_embeddings(collection):
    structured_table_file = "test_data/structured_table.csv"
    structured_data = pd.read_csv(structured_table_file)

    text_blob_file = "test_data/text_blob.txt"
    with open(text_blob_file, "r") as file:
        text_blob = file.read()

    # Process structured table into embeddings
    for idx, row in structured_data.iterrows():
        row_text = " ".join(map(str, row.values))
        embedding = generate_embedding(row_text)
        collection.add(
            documents=[row_text],
            embeddings=[embedding],
            ids=[f"structured_{idx}"],
            metadatas=[{"source": "structured_table"}]
        )

    # Process text blob into embeddings
    blob_id = "text_blob_1"
    blob_embedding = generate_embedding(text_blob)
    collection.add(
        documents=[text_blob],
        embeddings=[blob_embedding],
        ids=[blob_id],
        metadatas=[{"source": "text_blob"}]
    )

    print("Data successfully stored in ChromaDB.")

#chroma_client = PersistentClient(
#    path="chroma_persistent_storage",
#)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("vector_store")
store_embeddings(collection)

def query_vector_store(query_text, top_n=5):
    query_embedding = generate_embedding(query_text)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )
    return results

def search_chroma(query):
    nearest = query_vector_store(query)
    for doc, meta, dist in zip(nearest['documents'][0], nearest['metadatas'][0], nearest['distances'][0]):
        print(f"Document: {doc}, Source: {meta['source']}, Distance: {dist:.4f}")

search_chroma('parrot pair bonds')