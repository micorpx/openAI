# Release Notes Generator

Generates audience-specific release notes from git commits and issue trackers using an LLM.

## Quickstart
1. Copy repository files.
2. Create `.env` from `.env.example` and fill credentials.
3. `pip install -r requirements.txt`
4. Run: `python src/generate_notes.py --version v1.2.0 --audience users`

## Components
- `scripts/` — extract raw data from git and issue trackers
- `src/generate_notes.py` — core orchestration and LLM call
- `src/publish_to_confluence.py` — publish notes
- `.github/workflows/generate-release-notes.yml` — CI trigger on tag push

## Docker
Build and run:
```bash
docker build -t release-notes-generator:latest docker/
docker run --env-file .env -v $(pwd):/app release-notes-generator:latest
```

## License
MIT

## Tests & Linting

Run tests locally with `pytest` and lint with `flake8`.

## Frontend

A minimal Vite + React preview app is included in `frontend/`.

## Packaging

A zip archive of the project is created at `/mnt/data/release-notes-generator.zip` in this environment.
