import redis
from app.wrappers.LLMWrapper import LLMWrapper
from app.wrappers.RedisWrapper import RedisWrapper
from app.wrappers.EmbeddingWrapper import EmbeddingWrapper

redis_client = RedisWrapper()
LLM = LLMWrapper()
embedding_model = EmbeddingWrapper()