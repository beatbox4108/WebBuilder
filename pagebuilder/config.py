import yaml

def load() -> dict:
    with open("./pagebuild.yaml","r",encoding="utf-8")as f:config=yaml.safe_load(f)
    return config