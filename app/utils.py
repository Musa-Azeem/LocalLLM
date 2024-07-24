import json

def validate_request(request, fields):
    content_type = request.headers.get('Content-Type')
    if content_type is None or content_type != 'application/json':
        return False, {'mssg': 'Content-Type must be application/json'}
    
    json_data = request.get_json()
    if not json_data:
        return False, {'mssg': 'Request must contain JSON data'}

    empty_fields = [field for field in fields if field not in json_data]
    if empty_fields:
        return False, {'mssg': 'missing fields', 'missingFields': empty_fields}

    return True, json_data

def format_query(user_query, doc):
    return (
        f'DOCUMENT:\n{doc}\n'
        f'USER QUESTION:\n{user_query}\n'
    )