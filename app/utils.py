import json
import subprocess
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

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

def retrieve_and_parse_html(url, max_text_len):
    # Get the HTML page
    result = subprocess.run(
        ['wget', '--cipher', 'DEFAULT:!DH', '-q', '-O-', url], 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        return 'Invalid URL. Failed to retrieve the document'
    html_page = result.stdout.decode('utf-8')

    # Parse the HTML page
    try:
        soup = BeautifulSoup(html_page, 'html.parser')
        header_text = soup.find('div', id='topic-header').find('h1').text.strip()
        body = soup.find('div', id='topic-body')
    except Exception as e:
        return 'Failed to parse HTML File. Make sure it is a documentation page'
    text_sections = []

    def add_text(tag, section):
        if tag.name in ['p', 'li', 'td', 'th']:
            text = tag.text
            if text:
                section.append(text)
        elif tag.name in ['table', 'ul', 'ol']:
            for child in tag.children:
                add_text(child, section)

    for tag in body.find_all(['p', 'table', 'ul', 'ol']):
        section = []
        add_text(tag, section)
        if section:
            text_sections.append(section)

    # Split long sections into smaller parts
    entries = [header_text]
    for section in text_sections:
        for part in section:
            if len(part) <= max_text_len:
                entries.append(part)
            else:
                sentences = sent_tokenize(part)
                entry = ''
                for sentence in sentences:
                    if len(entry) + len(sentence) > max_text_len:
                        entries.append(entry)
                        entry = ''
                    entry += sentence

    return entries