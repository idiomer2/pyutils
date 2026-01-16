from urllib.parse import quote
from hashlib import md5
import requests

class TextDB:
    def __init__(self, base_url:str='https://textdb.online', hash_key:bool=False):
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.base_url = base_url.strip().rstrip('/')
        self.hash_key = hash_key

    def get_hash(self, key:str):
        return md5(key.encode('utf-8')).hexdigest() if self.hash_key else key

    def set(self, key:str, value:str):
        key = self.get_hash(key)
        url = f'{self.base_url}/update?key={key}'
        encoded_data = "value=" + quote(value)
        resp = requests.post(url, headers=self.headers, data=encoded_data)
        if resp.status_code == 200:
            return True
        else:
            print(f'resp.status_code={resp.status_code}, resp.reason={resp.reason}, resp.text={resp.text}')
            return False

    def get(self, key:str):
        key = self.get_hash(key)
        url = f'{self.base_url}/{key}'
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
        else:
            print(f'resp.status_code={resp.status_code}, resp.reason={resp.reason}, resp.text={resp.text}')
            return ""

    def delete(self, key:str):
        return self.set(key, "")
