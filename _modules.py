import json


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
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
