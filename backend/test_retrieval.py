import asyncio

from app.database.mongodb import knowledge_chunks_collection
from app.services.retrieval_service import (
    retrieve_relevant_chunks,
)


DATASET_ID = "dce0ca3f-49f6-487e-948b-6f4b6b99cf8e"


async def main():
    # Find a chunk that already has an embedding
    cursor = knowledge_chunks_collection.find(
        {
            "dataset_id": DATASET_ID,
            "embedding": {
                "$exists": True,
            },
        }
    )

    chunk = await cursor.to_list(length=1)

    if not chunk:
        print("No embedded chunks found")
        return

    # Use the user ID stored with the embedded chunk
    user_id = chunk[0]["user_id"]

    question = "What is Dataset 3 used for in BusinessPulse?"

    # Search the knowledge base for information related to the question
    results = await retrieve_relevant_chunks(
        question=question,
        dataset_id=DATASET_ID,
        user_id=user_id,
        top_k=3,
    )

    if not results:
        print("No relevant chunks found")
        return

    print("\nRetrieved chunks:\n")

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print("Similarity:", result["score"])
        print("Chunk index:", result["chunk_index"])
        print("Document ID:", result["document_id"])
        print("Text:")
        print(result["text"])
        print()


if __name__ == "__main__":
    asyncio.run(main())