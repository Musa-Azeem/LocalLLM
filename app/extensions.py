import redis
from app.LLMWrapper import LLMWrapper
from app.RedisWrapper import RedisWrapper

redis_client = RedisWrapper()
LLM = LLMWrapper()