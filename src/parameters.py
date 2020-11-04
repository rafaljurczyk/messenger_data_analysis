import json

params_file = 'params.json'

def getParam(paramKey: str, paramFile: str = params_file):
    with open(paramFile, "r", encoding='utf-8') as file:
        param = json.load(file)

    return param[paramKey]