from app.embedding_module import blueprint
from flask import request
from app.utils import validate_request
from app.extensions import embedding_model, vector_db_client
from flask import current_app
from app.utils import retrieve_and_parse_html

@blueprint.route('/embed_document', methods=['POST'])
def embed_document():
    valid, json_data = validate_request(request, ['url'])
    if not valid:
        return json_data, 400
    url = json_data['url']
    entries = retrieve_and_parse_html(url, current_app.config['MODEL_MAX_TOKENS'])
    if isinstance(entries, str):
        return dict(mssg=entries), 400
    try:
        doc_embeddings = embedding_model.encode_entries(entries)
    except Exception as e:
        print(e)
        return dict(mssg='Failed to embed document'), 500
    try:
        doc_id = vector_db_client.insert_doc(entries, url)
        vector_db_client.insert_entries(entries, doc_embeddings, doc_id)
    except Exception as e:
        print(e)
        return dict(mssg='Failed to add document/entries to DB'), 500
    
    return dict(mssg='Document embedded successfully'), 200