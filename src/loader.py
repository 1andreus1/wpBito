import json


def load_accounts():
    accounts_filepath = "accounts.json"
    with open(accounts_filepath) as file:
        json_data = json.load(file)
    
    data = [list(account.values()) for account in json_data.values()]
    return data

def load_ya_config():
    ya_config_filepath = "ya_config.json"
    with open(ya_config_filepath) as file:
        json_data = json.load(file)
    
    cookies, headers, params = json_data["cookies"], json_data["headers"], json_data["params"]
    
    return cookies, headers, params

def load_phrases():
    phrases_filepath = "./phrases.json"
    with open(phrases_filepath, encoding='utf-8') as file:
        phrases = json.load(file)
    return phrases

def save_hints(hints, append_mode=True):
    hints_filepath = "./hints.json"
    file_mode = "w+" if append_mode else "w"
    with open(hints_filepath, mode=file_mode, encoding='utf-8') as file:
        hints = json.dump(hints, file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))
    
def load_hints():
    hints_filepath = "./hints.json"
    with open(hints_filepath, encoding='utf-8') as file:
        hints = json.load(file)
    return hints