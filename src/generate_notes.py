"""Main orchestrator: collects data, prepares prompt, calls LLM, writes markdown."""
import argparse
import json
from datetime import date
from pathlib import Path
from src.utils import load_config, env
from scripts.extract_commits import extract_commits_local
from scripts.fetch_issues import fetch_github_issues
from scripts.classify_change import classify_commit

# LLM client placeholder - adapt to your provider
import openai

def build_prompt(version, commits, issues, audience):
    with open('templates/prompt.md') as f:
        tpl = f.read()
    data = tpl.format(version=version, date=str(date.today()), commits=json.dumps(commits[:200]), issues=json.dumps(issues[:200]), audience=audience)
    return data

def call_llm(prompt, model='gpt-5', temperature=0.0):
    openai.api_key = env('OPENAI_API_KEY')
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature,
        max_tokens=1500,
    )
    return resp['choices'][0]['message']['content']

def assemble_sections(llm_output: str) -> str:
    # If the LLM already returns markdown, use it directly. Optionally post-process.
    return llm_output

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--version', required=True)
    p.add_argument('--repo', default=None)
    p.add_argument('--audience', choices=['users', 'developers', 'managers'], default='users')
    args = p.parse_args()

    cfg = load_config()
    repo = args.repo or cfg.get('repo')
    commits = extract_commits_local('.')
    issues = fetch_github_issues(repo, env('GITHUB_TOKEN'))

    # basic classification
    for c in commits:
        c['type'] = classify_commit(c['subject'])

    prompt = build_prompt(args.version, commits, issues, args.audience)
    llm_out = call_llm(prompt, model=cfg['llm']['model'], temperature=cfg['llm'].get('temperature',0.0))

    md = assemble_sections(llm_out)
    out_file = Path('examples') / f'release_{args.version}.md'
    out_file.parent.mkdir(exist_ok=True)
    out_file.write_text(md, encoding='utf-8')
    print(f'Wrote {out_file}')
