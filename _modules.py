import json
import os
import requests

from dotenv import load_dotenv
load_dotenv()


class Quest:
    def __init__(self, test: str, reward=10, timeLimit=2, instruction="Missing"):
        self.test = test
        self.instruction = instruction or "Missing"
        self.reward = reward or 10
        self.timeLimit = timeLimit or 2

    def __repr__(self) -> dict:
        return {
            "gameClassOrder": int(self.test[17:19]),
            "name": self.test,
            "tests": [self.test],
            "instruction": self.instruction,
            "filter": f'test={self.test}',
            "timeLimit": self.timeLimit,
            "reward": self.reward
        }


def dump_to_json(file: str, data: dict):
    with open(file, mode='w') as f:
        f.write(json.dumps(data, indent=4))
        f.close()


def get_data_from_json(file: str):
    return json.loads(open(file).read())


HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-api-key": os.environ.get("API_KEY"),
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

API_URL = os.environ.get("API_URL")


def call_api(path, params={}) -> requests.Response:
    return requests.get(
        url=f'{API_URL}/{path}',
        params=params,
        headers=HEADERS
    )
