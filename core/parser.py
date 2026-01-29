import yaml

def parse(path):
    with open(path) as f:
        return yaml.safe_load(f)
