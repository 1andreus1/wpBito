import requests
from pprint import pprint
import multiprocessing
from loader import load_ya_config, load_phrases, save_hints


class HintParser():
    def __init__(self) -> None:
        self.MAIN_URL = "https://yandex.ru/suggest/suggest-ya.cgi"
        self.cookies, self.headers, self.params = load_ya_config()
        self.default_count = 30
    
    def update_hints(self):
        texts = load_phrases()
        hints = hintParser.get_hint_lists(texts)
        save_hints(hints)
        
    def get_hint_lists(self, texts, count=None):
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            hints = pool.map(self.get_hints, texts)
        hints = {k: v for d in hints for k, v in d.items()}
        return hints

    def get_hints(self, text, count=None):
        if not count:
            count = self.default_count
        
        self.params["n"] = count
        self.params["part"] = text

        response = requests.get(
            self.MAIN_URL,
            params=self.params,
            # cookies=cookies,
            # headers=headers,
        )
        res_json = response.json()
        res_json = {res_json[0]: [hint[1] for hint in res_json[1]]}
        return res_json


if __name__ == "__main__":
    hintParser = HintParser()
    hintParser.update_hints()
