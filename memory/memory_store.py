from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.chromadb import (
    ChromaDBVectorMemory,
    PersistentChromaDBVectorMemoryConfig,
    CustomEmbeddingFunctionConfig,
)
from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
import os
from dotenv import load_dotenv
load_dotenv()

def get_gemini_embedding_function():
    return GoogleGenerativeAiEmbeddingFunction(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model_name="models/embedding-001"  # gemini embedding model
    )

def memory_model():

    chroma_user_memory = ChromaDBVectorMemory(
        config=PersistentChromaDBVectorMemoryConfig(
            collection_name="resume_scores",
            persistence_path="./chroma_resume_db",  # Use the temp directory here
            k=1,  # Return top k results
            score_threshold=0.8,  # Minimum similarity score
            embedding_function_config=CustomEmbeddingFunctionConfig(
                function=get_gemini_embedding_function
            ),
        )
    )
    
    return chroma_user_memory