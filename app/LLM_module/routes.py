from app.LLM_module import blueprint
from flask import request
from app.utils import validate_request

@blueprint.route('/chatbot', methods=['POST'])
def chatbot():
    valid, json_data = validate_request(request, ['message'])
    if not valid:
        return json_data, 400
    print(json_data)
    return dict(mssg='Chatbot response'), 200