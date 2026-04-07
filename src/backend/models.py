"""
HomeBuddy AI Models Module
Handles loading and inference for embedding models, FAISS indexing, and LLM responses
"""

import logging
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available - install with: pip install sentence-transformers")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("faiss-cpu not available - install with: pip install faiss-cpu")


class EmbeddingModel:
    """Handles embeddings using sentence transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.available = False
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"Loading embedding model: {model_name}")
                self.model = SentenceTransformer(model_name)
                self.available = True
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                
    def encode(self, texts: List[str]) -> Optional[np.ndarray]:
        """Encode texts to embeddings"""
        if not self.available or not self.model:
            return None
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding texts: {e}")
            return None
            
    def encode_single(self, text: str) -> Optional[np.ndarray]:
        """Encode single text to embedding"""
        if not self.available or not self.model:
            return None
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            return None


class FAISSRetriever:
    """Handles FAISS-based retrieval of relevant chunks"""
    
    def __init__(self, embedding_model: EmbeddingModel, data_file: str = "data_processed/manual_chunks.jsonl"):
        self.embedding_model = embedding_model
        self.index = None
        self.chunks = []
        self.data_file = Path(data_file)
        self.available = False
        
        if embedding_model.available:
            self._load_chunks()
            if self.chunks:
                self._build_index()
                
    def _load_chunks(self):
        """Load chunks from JSONL file"""
        if not self.data_file.exists():
            logger.warning(f"Data file not found: {self.data_file}")
            return
            
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        chunk = json.loads(line)
                        self.chunks.append(chunk)
            logger.info(f"Loaded {len(self.chunks)} chunks from {self.data_file}")
        except Exception as e:
            logger.error(f"Error loading chunks: {e}")
            
    def _build_index(self):
        """Build FAISS index from chunks"""
        if not self.chunks or not self.embedding_model.available:
            return
            
        try:
            # Get embeddings for all chunks
            texts = [chunk.get('text', '') for chunk in self.chunks]
            embeddings = self.embedding_model.encode(texts)
            
            if embeddings is None:
                logger.warning("Failed to generate embeddings for chunks")
                return
                
            # Create FAISS index
            embedding_dim = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(embedding_dim) if FAISS_AVAILABLE else None
            
            if self.index:
                embeddings_normalized = embeddings.astype(np.float32)
                self.index.add(embeddings_normalized)
                self.available = True
                logger.info(f"FAISS index built with {len(self.chunks)} chunks, dimension: {embedding_dim}")
        except Exception as e:
            logger.error(f"Error building FAISS index: {e}")
            
    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve top-k relevant chunks"""
        if not self.available or not self.index or not self.chunks:
            logger.debug("FAISS retriever not available or empty")
            return []
            
        try:
            # Encode query
            query_embedding = self.embedding_model.encode_single(query)
            if query_embedding is None:
                return []
                
            # Search
            query_embedding = np.array([query_embedding], dtype=np.float32)
            distances, indices = self.index.search(query_embedding, min(k, len(self.chunks)))
            
            # Collect results
            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0:  # Valid index
                    chunk = self.chunks[idx].copy()
                    chunk['distance'] = float(distance)
                    chunk['relevance_score'] = 1.0 / (1.0 + float(distance))  # Convert distance to score
                    results.append(chunk)
                    
            return results
        except Exception as e:
            logger.error(f"Error retrieving chunks: {e}")
            return []


class LLMGenerator:
    """Handles LLM-based answer generation"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.available = False
        self.use_openai = False
        
        if api_key:
            try:
                import openai
                openai.api_key = api_key
                self.use_openai = True
                self.available = True
                logger.info(f"OpenAI LLM initialized with model: {model}")
            except Exception as e:
                logger.warning(f"Could not initialize OpenAI: {e}")
                
    def generate_answer(self, query: str, chunks: List[Dict], brand: Optional[str] = None, 
                       model: Optional[str] = None, max_tokens: int = 1000) -> str:
        """Generate answer using LLM and retrieved chunks"""
        
        if not chunks:
            return self._generate_fallback(query, brand, model)
            
        try:
            # Prepare context
            context = "\n".join([chunk.get('text', '') for chunk in chunks[:5]])  # Use top 5
            
            if self.use_openai:
                return self._call_openai(query, context, brand, model, max_tokens)
            else:
                return self._generate_fallback(query, brand, model, context)
                
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return self._generate_fallback(query, brand, model)
    
    def _call_openai(self, query: str, context: str, brand: Optional[str], 
                     model_name: Optional[str], max_tokens: int) -> str:
        """Call OpenAI API for answer generation"""
        try:
            import openai
            
            device_ref = f" for {brand} {model_name}" if brand and model_name else ""
            
            prompt = f"""You are an expert appliance repair assistant. Based on the provided knowledge base, 
answer the user's question about appliance troubleshooting in clear, detailed steps.

Knowledge Base:
{context}

User Question: {query}{device_ref}

Please provide:
1. Detailed troubleshooting steps
2. Safety warnings if applicable
3. When to call a professional
4. Prevention tips

Answer:"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert appliance repair technician providing detailed troubleshooting guidance."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI: {e}")
            return self._generate_fallback(query, brand, model_name)
    
    def _generate_fallback(self, query: str, brand: Optional[str] = None, 
                          model: Optional[str] = None, context: str = "") -> str:
        """Generate fallback answer using rule-based approach"""
        # This uses the comprehensive guides already defined
        # Enhanced with retrieved context if available
        query_lower = query.lower()
        
        base_answer = f"Troubleshooting assistance for {brand} {model}\n\n" if brand and model else ""
        
        if context:
            base_answer += f"Based on knowledge base:\n{context[:500]}...\n\n"
            
        if "not working" in query_lower:
            base_answer += """**Basic Troubleshooting Steps:**
1. Check power connection and outlet
2. Verify appliance is turned on
3. Check circuit breaker
4. Inspect power cord for damage
5. Reset by unplugging for 5 minutes"""
        elif "leak" in query_lower:
            base_answer += """**Water Leak Troubleshooting:**
1. Turn off and unplug immediately
2. Locate the leak source
3. Check hose connections and seals
4. Clean drain filter
5. Inspect door gasket"""
        elif "noise" in query_lower:
            base_answer += """**Noise Troubleshooting:**
1. Identify noise type (grinding, squealing, clicking)
2. Check for foreign objects
3. Ensure appliance is level
4. Check loose parts
5. Look for worn bearings or belts"""
        else:
            base_answer += """**General Troubleshooting:**
1. Check power and basic connections
2. Reset the appliance
3. Consult user manual for error codes
4. Clean filters and drains
5. Contact professional if issue persists"""
            
        return base_answer
