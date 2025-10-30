"""Publish a markdown file to Confluence via REST API (example)."""
import os
import requests
from src.utils import env, load_config

CFG = load_config()
BASE = env('CONFLUENCE_BASE')
USER = env('CONFLUENCE_USER')
TOKEN = env('CONFLUENCE_API_TOKEN')
SPACE = CFG['publish']['confluence_space']
PARENT_ID = CFG['publish']['confluence_parent_page_id']

def md_to_storage_format(md: str) -> dict:
    return {
        'type': 'page',
        'title': 'Release Notes',
        'space': {'key': SPACE},
        'ancestors': [{'id': PARENT_ID}],
        'body': {
            'storage': {
                'value': '<pre>' + md.replace('<', '&lt;').replace('>', '&gt;') + '</pre>',
                'representation': 'storage'
            }
        }
    }

def publish(version: str, md_path: str):
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()
    payload = md_to_storage_format(md)
    url = f'{BASE}/rest/api/content'
    r = requests.post(url, auth=(USER, TOKEN), json=payload)
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    import sys
    ver = sys.argv[1]
    path = sys.argv[2]
    print(publish(ver, path))
