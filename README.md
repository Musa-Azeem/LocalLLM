# Run App:

- Start Redis Server: `docker run --name llm_redis -p 6379:6379 -it redis`
- Start Qdrant Server: `docker run --name vectordb -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant`
- Start flask: `python3 run_debug_server.py`