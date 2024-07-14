from app.session_module import blueprint
from app.extensions import redis_client
import secrets
from flask import current_app
from datetime import datetime
from flask import request
from app.utils import validate_request

@blueprint.route('/start_session')
def start_session():
    session_id = secrets.token_hex(16)
    try:
        # redis_client.hset(session_id, 'time_created', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        redis_client.hset(session_id, 'n_chats', 0)
        redis_client.expire(session_id, current_app.config['SESSION_TIMEOUT'])
    except:
        return dict(mssg='Session creation failed'), 500
    return dict(mssg='Session started', session_id=session_id), 200

@blueprint.route('/end_session')
def end_session():
    valid, json_data = validate_request(request, ['message'])
    if not valid:
        return json_data, 400
    session_id = json_data['session_id']

    redis_client.delete(session_id)
    return dict(mssg='Session ended'), 200