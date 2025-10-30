import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config(path='config.yaml'):
    with open(path) as f:
        return yaml.safe_load(f)

def env(key, default=None):
    return os.getenv(key, default)
