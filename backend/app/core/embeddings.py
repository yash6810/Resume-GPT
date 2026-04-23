import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict
import faiss
import os


class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the embedding model."""
        self.model_name = model_name
        self.model = None
        self.index = None
        self.skills = []
        self.embeddings = None

    def load_model(self):
        """Load the sentence transformer model."""
        if self.model is None:
            print(f"Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print("Model loaded successfully")

    def encode_texts(self, texts: List[str]) -> np.ndarray:
        """Encode a list of texts into embeddings."""
        self.load_model()
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text into embedding."""
        self.load_model()
        embedding = self.model.encode([text], convert_to_numpy=True)
        return embedding[0]

    def build_skill_index(self, skills: List[str]):
        """Build FAISS index for skills."""
        self.skills = skills
        self.embeddings = self.encode_texts(skills)

        # Build FAISS index
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(
            dimension
        )  # Inner product (cosine similarity after normalization)

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings)

        print(f"Built FAISS index with {len(skills)} skills")

    def find_similar_skills(
        self, query: str, top_k: int = 5, threshold: float = 0.6
    ) -> List[Tuple[str, float]]:
        """Find similar skills to a query."""
        if self.index is None or not self.skills:
            return []

        # Encode query
        query_embedding = self.encode_single(query)
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)

        # Search
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= threshold:
                results.append((self.skills[idx], float(score)))

        return results

    def cosine_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts."""
        emb1 = self.encode_single(text1)
        emb2 = self.encode_single(text2)

        # Normalize
        emb1 = emb1 / np.linalg.norm(emb1)
        emb2 = emb2 / np.linalg.norm(emb2)

        return float(np.dot(emb1, emb2))


# Global embedding model instance
embedding_model = EmbeddingModel()


def get_embedding_model() -> EmbeddingModel:
    """Get the global embedding model instance."""
    return embedding_model
