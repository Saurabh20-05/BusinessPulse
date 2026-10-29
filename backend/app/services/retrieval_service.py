from app.database.mongodb import (
    knowledge_chunks_collection,
)
from app.services.embedding_service import (
    generate_embedding,
)


# Number of relevant chunks returned for each question
DEFAULT_TOP_K = 3


def calculate_similarity(
    query_embedding: list[float],
    chunk_embedding: list[float],
) -> float:
    # Both embeddings are normalized, so their dot product gives cosine similarity
    return sum(
        query_value * chunk_value
        for query_value, chunk_value in zip(
            query_embedding,
            chunk_embedding,
        )
    )


async def retrieve_relevant_chunks(
    question: str,
    dataset_id: str,
    user_id: str,
    top_k: int = DEFAULT_TOP_K,
):
    # Convert the user's question into the same vector format as stored chunks
    query_embedding = generate_embedding(question)

    # Only retrieve chunks belonging to the current user and selected dataset
    cursor = knowledge_chunks_collection.find(
        {
            "dataset_id": dataset_id,
            "user_id": user_id,
        }
    )

    chunks = await cursor.to_list(length=None)

    if not chunks:
        return []

    # Compare the question embedding with every available knowledge chunk
    scored_chunks = []

    for chunk in chunks:
        embedding = chunk.get("embedding")

        if not embedding:
            continue

        similarity = calculate_similarity(
            query_embedding,
            embedding,
        )

        scored_chunks.append(
            {
                "text": chunk["text"],
                "score": similarity,
                "chunk_index": chunk["chunk_index"],
                "document_id": chunk["document_id"],
                "file_id": chunk["file_id"],
            }
        )

    # Highest similarity means the chunk is most relevant to the question
    scored_chunks.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_chunks[:top_k]