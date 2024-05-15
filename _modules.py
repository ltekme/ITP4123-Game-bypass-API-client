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
