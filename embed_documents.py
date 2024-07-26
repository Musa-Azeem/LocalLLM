import subprocess
from bs4 import BeautifulSoup
import requests

result = subprocess.run(
    ['wget', '--cipher', 'DEFAULT:!DH', '-q', '-O-', 'https://docs.us.sios.com/spslinux/9.8.1/en/topic/sios-protection-suite-for-linux'], 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

soup = BeautifulSoup(result.stdout.decode('utf-8'), 'html.parser')
sidebar = soup.find('ul', id='manual-toc')

urls = [a['href'] for a in sidebar.find_all('a', href=True)]
urls = urls[1:100]
print([f'{u}\n' for u in urls])
for url in urls:
    print(url)
    requests.post(
        'http://localhost:8000/embed_document',
        json={
            'url': url,
        }
    )