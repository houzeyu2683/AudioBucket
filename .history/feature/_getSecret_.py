import yaml

def getSecret(path: str) -> dict:
    with open(path, 'r') as paper:
        secret = yaml.load(paper, yaml.SafeLoader)
        pass
    return(secret)