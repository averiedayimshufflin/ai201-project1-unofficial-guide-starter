import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


CHUNKS_FILE = Path("data/chunks.json")
CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "umd_cs_prof_reviews"


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Remove empty or bad chunks before embedding
    cleaned_chunks = []
    for chunk in chunks:
        text = chunk.get("text", "").strip()

        if not text:
            continue

        if len(text.split()) < 10:
            continue

        if "Professor TA Expected Grade" in text:
            continue

        cleaned_chunks.append(chunk)

    return cleaned_chunks


def build_vector_store():
    print("Loading chunks...")
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete old collection if it exists, so reruns do not duplicate data
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
    )
    texts = []
    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        text = chunk["text"]

        texts.append(text)
        ids.append(chunk.get("chunk_id", f"chunk_{i}"))

        metadatas.append({
            "source": chunk.get("source", ""),
            "url": chunk.get("url", ""),
            "chunk_id": chunk.get("chunk_id", f"chunk_{i}"),
            "chunk_type": chunk.get("chunk_type", ""),
            "token_count": chunk.get("token_count", 0),
            "position": i,
        })

    print("Embedding chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    print("Adding chunks to ChromaDB...")
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Saved {len(texts)} chunks to ChromaDB")
    return collection, model


def load_vector_store():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)
    return collection, model


def retrieve(query, collection, model, k=5):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    retrieved = []

    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved.append({
            "text": doc,
            "metadata": metadata,
            "distance": distance,
        })

    return retrieved


def print_results(query, results):
    print("\n" + "=" * 100)
    print(f"QUERY: {query}")
    print("=" * 100)

    for i, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(f"\nResult {i}")
        print("-" * 100)
        print(f"Distance: {result['distance']:.4f}")
        print(f"Source: {metadata['source']}")
        print(f"URL: {metadata['url']}")
        print(f"Chunk ID: {metadata['chunk_id']}")
        print("-" * 100)
        print(result["text"][:1200])


def main():
    collection, model = build_vector_store()

    test_queries = [
        "What CMSC courses expect a heavy workload or mention difficult projects?",
        "What official course policies from Christopher Kauffman's CMSC216 page might explain student comments about workload?",
        "What do students say about Larry Herman's teaching style in CMSC132 or CMSC216?",
    ]

    for query in test_queries:
        results = retrieve(query, collection, model, k=5)
        print_results(query, results)


if __name__ == "__main__":
    main()