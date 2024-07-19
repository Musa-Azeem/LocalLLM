import bs4
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
from pathlib import Path
import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse
nltk.download('punkt')

MAX_TEXT_LEN = 512
MODEL_NAME = "infgrad/stella_en_400M_v5"
EMB_DIM = 1024
DEVICE = 'cuda'
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "LLM_embedding"

if len(sys.argv) < 3:
    print("Usage: python embed_document.py <path_to_html_file> <doc_url>")
    sys.exit(1)

html_file = Path(sys.argv[1])
url = sys.argv[2]

print('Loading model...')
model = SentenceTransformer(MODEL_NAME, trust_remote_code=True).to(DEVICE)
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Parse HTML
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    header_text = soup.find('div', id='topic-header').find('h1').text.strip()
    body = soup.find('div', id='topic-body')
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
    
    return header_text, text_sections

print('Parsing HTML...')
html_page = html_file.open().read()
header_text, text_sections = parse_html(html_page)

entries = [header_text]
for section in text_sections:
    for part in section:
        if len(part) <= MAX_TEXT_LEN:
            entries.append(part)
        else:
            sentences = sent_tokenize(part)
            entry = ''
            for sentence in sentences:
                if len(entry) + len(sentence) > MAX_TEXT_LEN:
                    entries.append(entry)
                    print(entry)
                    entry = ''
                entry += sentence

# Embed entries
print('Embedding entries...')
doc_embeddings = model.encode(entries, device="cuda")

# Add entries to vector DB
print('Adding entries to vector DB...')
try:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=EMB_DIM, distance=Distance.DOT),
    )
except UnexpectedResponse as e:
    print('Collection exists')

points = [PointStruct(
    id=i, 
    vector=doc_embeddings[i],
    payload={'text': entries[i], 'url': url}
) for i in range(len(entries))]

operation_info = client.upsert(
    collection_name=COLLECTION_NAME,
    wait=True,
    points=points,
)

print('Done')