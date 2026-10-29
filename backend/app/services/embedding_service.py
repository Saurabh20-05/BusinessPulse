from sentence_transformers import SentenceTransformer


# Small general-purpose model that works well for semantic text search
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    # Convert the text chunk into a numerical vector
    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    # Convert NumPy values into normal Python floats for MongoDB
    return embedding.tolist()