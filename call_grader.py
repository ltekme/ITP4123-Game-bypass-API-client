import time
import requests
import json
import os
from dotenv import load_dotenv
from _modules import dump_to_json, get_data_from_json, call_api
load_dotenv()


def get_api_key():
    api_key = os.environ.get('API_KEY')
    if api_key is None:
        raise Exception("api_key is required.")
    return api_key


def _get_finished_quests():
    api_response = call_api(path="getpassedtest")
    if api_response.status_code != 200:
        raise Exception(f"Error: {api_response.status_code}")
    return json.loads(str(api_response.content.decode('utf-8')))


def _get_unfinished_quests():
    while True:
        api_response = call_api(path="game?mode")
        if api_response.status_code != 200:
            raise Exception(f"Error: {api_response.status_code}")
        data = api_response.content.decode('utf-8')
        if "[" not in data:
            continue
        return json.loads(str(data))


def _get_test_resault(filter: str, logdir: str):
    api_response = call_api(path="grader", params={
        "filter": filter
    })
    if api_response.status_code != 200:
        raise Exception(f"Error: {api_response.status_code}")
    resault = json.loads(str(api_response.content.decode('utf-8')))
    if resault['isSuccess'] is False:
        log = requests.get(resault['logUrl']).content.decode('utf-8')
        logPath = f'{logdir}/{filter.split("=")[1]}/{int(time.time())}.txt'
        if not os.path.exists(os.path.dirname(logPath)):
            os.makedirs(os.path.dirname(logPath))
        with open(logPath, mode='w') as f:
            f.write(f'{log}\n')
        return False, log
    return True, None


def main(quests_file: str, ignore_file: str, finish_file: str, log_dir: str):
    api_key = get_api_key()

    if not os.path.exists(quests_file):
        dump_to_json(quests_file, _get_unfinished_quests())
    if not os.path.exists(finish_file):
        dump_to_json(finish_file, _get_finished_quests())
    if not os.path.exists(ignore_file):
        dump_to_json(ignore_file, [])

    quests = get_data_from_json(quests_file)
    completed_quests = get_data_from_json(finish_file)
    ignore_quests = get_data_from_json(ignore_file)

    finished_tests = [test['test'] for test in completed_quests]
    ignore_tests = [test['tests'][0] for test in ignore_quests]

    # Filters
    quests = [q for q in quests if q['tests'][0]
              not in finished_tests]  # filter finished
    quests = [q for q in quests if q['tests'][0]
              not in ignore_tests]  # filter ignored

    print(f"Testing {quests[0]['name']}")
    resault = _get_test_resault(filter=quests[0]['filter'], logdir=log_dir)
    lines = '*' * 100
    space = '\n' * 2
    if resault[0]:
        dump_to_json(finish_file, _get_finished_quests())
        print(f"{lines}{space}{quests[0]} Passed{space}{lines}{
            space}{quests[1]['name']} instruction{space}{quests[1]['instruction']}{space}{lines}")
    else:
        print(f"{lines}{space}{resault[1]}{space}{lines}{
            space}{quests[0]['instruction']}{space}{lines}")


if __name__ == '__main__':
    configs = {
        'finish_file': './data/finished.json',
        'quests_file': './data/quests.json',
        'ignore_file': './data/ignore.json',
        'log_dir': "./data"
    }
    main(**configs)
