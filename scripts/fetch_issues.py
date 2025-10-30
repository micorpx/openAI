"""Fetch issues from GitHub or Jira. This example shows GitHub issues via REST API."""
import os
import requests
from typing import List

def fetch_github_issues(repo: str, token: str, state: str = 'closed') -> List[dict]:
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/repos/{repo}/issues?state={state}&per_page=100'
    issues = []
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        issues.extend(r.json())
        link = r.headers.get('Link')
        if link and 'rel="next"' in link:
            parts = [p.split(';') for p in link.split(',')]
            url = None
            for p in parts:
                if 'rel="next"' in p[1]:
                    url = p[0].strip().strip('<>').strip()
        else:
            url = None
    return issues

if __name__ == '__main__':
    import json, os
    repo = os.getenv('REPO', 'owner/repo')
    token = os.getenv('GITHUB_TOKEN')
    data = fetch_github_issues(repo, token)
    print(json.dumps(data[:20], indent=2))
