from typing import List, Optional
import numpy as np

class EmbeddingService:
    """Service for generating and working with embeddings."""
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize the embedding service with a model.
        
        Args:
            model_name: Name of the pre-trained model to use
        """
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except ImportError:
            print("SentenceTransformers package not installed. Using fallback embedding method.")
            self.model = None
    
    def encode(self, text: str) -> Optional[np.ndarray]:
        """
        Generate an embedding for the given text.
        
        Args:
            text: Text to encode
            
        Returns:
            Embedding vector or None if no model is available
        """
        if self.model is None:
            return self._fallback_encode(text)
            
        return self.model.encode(text)
    
    def _fallback_encode(self, text: str) -> Optional[np.ndarray]:
        """
        Simple fallback encoding method when no model is available.
        This is just a placeholder and not suitable for production.
        
        Args:
            text: Text to encode
            
        Returns:
            Simple representation vector
        """
        # Count character frequencies as a simple embedding
        # This is not a good embedding but serves as a placeholder
        chars = {}
        for char in text.lower():
            if char.isalnum():
                chars[char] = chars.get(char, 0) + 1
                
        # Create a fixed-size vector (26 lowercase letters + 10 digits)
        vector = np.zeros(36)
        for i, char in enumerate("abcdefghijklmnopqrstuvwxyz0123456789"):
            vector[i] = chars.get(char, 0)
            
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return vector
        
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate the cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0-1)
        """
        # Reshape to 2D if needed
        if embedding1.ndim == 1:
            embedding1 = embedding1.reshape(1, -1)
        if embedding2.ndim == 1:
            embedding2 = embedding2.reshape(1, -1)
            
        # Calculate cosine similarity
        dot_product = np.dot(embedding1, embedding2.T)[0][0]
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
            
        return dot_product / (norm1 * norm2)