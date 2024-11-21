import time
import requests
import json
import os
from _modules import dump_to_json, get_data_from_json, call_api
from _modules import get_data_from_json


def _get_unfinished_quests():
    while True:
        api_response = call_api(path="game?mode")
        if api_response.status_code != 200:
            raise Exception(f"Error: {api_response.status_code}")
        data = api_response.content.decode('utf-8')
        if "[" not in data:
            continue
        return json.loads(str(data))


if __name__ == "__main__":
    quests_file = './data/quests.json'

    if not os.path.exists(quests_file):
        dump_to_json(quests_file, _get_unfinished_quests())

    quests = get_data_from_json(quests_file)

    for i in quests:
        print('*'*50)
        test_name = i['tests'][0]
        dot_test = test_name.find(".Test")
        print(f"{test_name[16:19]}_{test_name[dot_test+1:dot_test+7]}")
        print(i['instruction'])
        print("\n")
