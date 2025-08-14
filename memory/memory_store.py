from autogen_core.memory import MemoryContent, MemoryMimeType
from autogen_ext.memory.redis import RedisMemory, RedisMemoryConfig


def memory_store(resume_score):
    try:
        redis_memory = RedisMemory(
        config=RedisMemoryConfig(
            redis_url="redis://localhost:6379",
            index_name="chat_history",
            prefix="memory",
        )
    )
        redis_memory.add(
            content = resume_score,
            mime_type = MemoryMimeType.TEXT,
            metadata={"category": "resume"}
        )
    
        return redis_memory
    except Exception as e:
        print(f"Error occured during initializing memory_store: {e}")