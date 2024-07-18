import redis

class RedisWrapper():
    def __init__(self):
        self.client = None
    
    def init_app(self, app):
        self.client = redis.Redis(
            host=app.config['REDIS_HOST'], 
            port=app.config['REDIS_PORT'], 
            db=0, 
            decode_responses=True
        )

    def hset(self, key, field, value):
        self.client.hset(key, field, value)
    
    def hget(self, key, field):
        return self.client.hget(key, field)
    
    def hgetall(self, key):
        return self.client.hgetall(key)
    
    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)

    def expire(self, key, timeout):
        self.client.expire(key, timeout)

    def delete(self, key):
        self.client.delete(key)

    def ping(self):
        self.client.ping()