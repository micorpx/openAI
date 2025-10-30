FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Expose nothing by default; the entrypoint runs a test generation
CMD ["python", "src/generate_notes.py", "--version", "dev-local"]
