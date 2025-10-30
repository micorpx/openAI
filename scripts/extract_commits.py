"""Extract commits from a local repo or via GitHub API."""
import subprocess
from typing import List, Dict

def extract_commits_local(path: str = '.', since: str | None = None) -> List[Dict]:
    cmd = [
        'git', '-C', path, 'log', '--pretty=format:%H|%an|%s|%b|%cd'
    ]
    if since:
        cmd.insert(-1, f'--since={since}')
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL)
    commits = []
    for line in out.splitlines():
        parts = line.split('|', 4)
        commits.append({
            'hash': parts[0], 'author': parts[1], 'subject': parts[2], 'body': parts[3], 'date': parts[4]
        })
    return commits

if __name__ == '__main__':
    import json
    commits = extract_commits_local('.')
    print(json.dumps(commits[:50], indent=2))
