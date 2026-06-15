import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_DIR = "data/chroma_db"
COLLECTION_NAME = "umd_cs_prof_reviews"
MODEL_NAME = "llama-3.3-70b-versatile"


def load_retriever():
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    return embedder, collection


embedder, collection = load_retriever()
groq_client = Groq()


def retrieve(question, k=5):
    query_embedding = embedder.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []

    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text": text,
            "source": metadata.get("source", "Unknown source"),
            "url": metadata.get("url", ""),
            "chunk_id": metadata.get("chunk_id", ""),
            "distance": distance,
        })

    return chunks


def build_context(chunks):
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}]\n"
            f"Source name: {chunk['source']}\n"
            f"URL: {chunk['url']}\n"
            f"Chunk ID: {chunk['chunk_id']}\n"
            f"Text: {chunk['text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question, chunks):
    context = build_context(chunks)

    system_prompt = """
You are a grounded question-answering assistant.

Rules:
- Answer using ONLY the provided retrieved context.
- Do not use outside knowledge.
- If the retrieved context does not contain enough information, say: "I don't have enough information on that."
- Do not invent professor names, ratings, course facts, or policies.
- Keep the answer concise.
- Mention the source names that support the answer.
"""

    user_prompt = f"""
Question:
{question}

Retrieved context:
{context}

Answer:
"""

    response = groq_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content


def ask(question):
    chunks = retrieve(question, k=5)
    answer = generate_answer(question, chunks)

    sources = []
    seen = set()

    for chunk in chunks:
        key = (chunk["source"], chunk["url"])

        if key not in seen:
            seen.add(key)
            sources.append({
                "source": chunk["source"],
                "url": chunk["url"],
                "distance": round(chunk["distance"], 4),
            })

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source['source']} ({source['url']}) distance={source['distance']}")