from app.LLM_module import blueprint
from flask import request
from app.utils import validate_request
from app.extensions import LLM, redis_client, embedding_model, vector_db_client
from flask import current_app
from app.utils import format_query

@blueprint.route('/prompt', methods=['POST'])
def prompt():
    valid, json_data = validate_request(request, ['message'])
    if not valid:
        return json_data, 400
    response = LLM.create_chat_completion(
        messages=[
            {'role': 'system', 'content': current_app.config['SYSTEM_MESSAGE']},
            {'role': 'user', 'content': json_data['message']}
        ]
    )
    response = response['choices'][0]['message']['content']
    return dict(response=response), 200

@blueprint.route('/chat', methods=['POST'])
def chat():
    valid, json_data = validate_request(request, ['message'])
    if not valid:
        return json_data, 400
    message = json_data['message']
    if len(message) == 0:
        return dict(mssg='Empty Query'), 400
    
    chats = [{'role': 'system', 'content': current_app.config['SYSTEM_MESSAGE']}]
    
    try:
        response, chosen_url, urls = embed_query_and_generate(chats, message)
    except Exception as e:
        print(e, type(e))
        return dict(mssg='Chat completion failed'), 500
    
    
    return dict(response=response, url=chosen_url, other_urls=urls), 200

@blueprint.route('/chat_completion', methods=['POST'])
def chat_completion():
    valid, json_data = validate_request(request, ['message', 'session_id'])
    if not valid:
        return json_data, 400
    session_id = json_data['session_id']
    message = json_data['message']
    if len(message) == 0:
        return dict(mssg='Empty Query'), 400
    
    chats = [{'role': 'system', 'content': current_app.config['SYSTEM_MESSAGE']}]
    
    try:
        n_chats = int(redis_client.hget(session_id, 'n_chats'))
        for i in range(n_chats):
            chats.append({'role': 'user', 'content': redis_client.hget(session_id, f'chat_{i}')})
    except:
        return dict(mssg='Session not found'), 404
    
    try:
        response, chosen_url, urls = embed_query_and_generate(chats, message)
    except Exception as e:
        print(e, type(e))
        return dict(mssg='Chat completion failed'), 500
    
    try:
        redis_client.hset(session_id, f'chat_{n_chats}', message)
        redis_client.hset(session_id, 'n_chats', n_chats+1)
    except:
        return dict(mssg='Chat storage failed'), 500
    
    return dict(response=response, url=chosen_url, other_urls=urls), 200

def embed_query_and_generate(chats, message):
        embedding = embedding_model.encode_query([message])
        top_k = vector_db_client.search(embedding[0], top_k=current_app.config['SEARCH_TOP_K'])
        text = 'No document'
        chosen_url = None
        urls = []
        if top_k is not None:
            for entry in top_k:
                doc_id = entry.payload['doc_id']
                doc = vector_db_client.get_doc(doc_id)
                if doc:
                    # if first match with a document, use text 
                    if text == 'No document':
                        text = doc.payload['text']
                        chosen_url = doc.payload['url']
                    else:
                        # for all k, get the urls
                        urls.append(doc.payload['url'])
        chats.append({
            'role': 'user',
            'content': format_query(message, text)
        })
        response = LLM.create_chat_completion(messages=chats)
        response = response['choices'][0]['message']['content']
        return response, chosen_url, urls