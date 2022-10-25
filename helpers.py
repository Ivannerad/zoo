import json
from variables import PROJECT_DIR


def read_config():
    with open(f'{PROJECT_DIR}/config.json', 'r') as f:
        cfg = json.loads(f.read())
    return cfg