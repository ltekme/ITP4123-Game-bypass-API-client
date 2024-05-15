import requests
import json
import os
from urllib.parse import quote_plus
from dotenv import dotenv_values
from _modules import dump_to_json, get_data_from_json

API_URL = 'https://kp4du9furk.execute-api.us-east-1.amazonaws.com/api'


def get_api_key(api_key: str = None):
    if api_key is None:
        api_key = os.environ.get('API_KEY')
        if api_key is None:
            raise Exception("api_key is required.")
    return api_key


def _get_finished_quests(api_key: str = None):
    api_response = requests.get(
        f'{API_URL}/marks?api_key={quote_plus(get_api_key(api_key))+"&"}')
    if api_response.status_code != 200:
        raise Exception(f"Error: {api_response.status_code}")
    return json.loads(str(api_response.content.decode('utf-8')))


def _get_unfinished_quests(api_key: str = None):
    while True:
        api_response = requests.get(
            f'{API_URL}/game?api_key={quote_plus(get_api_key(api_key))+"&"}')
        if api_response.status_code != 200:
            raise Exception(f"Error: {api_response.status_code}")
        data = api_response.content.decode('utf-8')
        if "[" not in data:
            continue
        return json.loads(str(data))


def _get_test_resault(filter: str, api_key: str = None):
    api_response = requests.get(
        f'{API_URL}/grader', params={'api_key': get_api_key(api_key), "filter": filter})
    if api_response.status_code != 200:
        raise Exception(f"Error: {api_response.status_code}")
    resault = json.loads(str(api_response.content.decode('utf-8')))
    if resault['isSuccess'] is False:
        log = requests.get(resault['logUrl']).content.decode('utf-8')
        with open('latest_log.txt', mode='w') as f:
            f.write(f'{log}\n')
        return False, log
    return True, None


def main(quests_file: str, ignore_file: str , finish_file: str, api_key: str = None):
    api_key = get_api_key(api_key)

    if not os.path.exists(quests_file):
        dump_to_json(quests_file, _get_unfinished_quests(api_key))
    if not os.path.exists(finish_file):
        dump_to_json(quests_file, _get_finished_quests(api_key))
    if not os.path.exists(ignore_file):
        dump_to_json(quests_file, [])

    quests, completed_quests = get_data_from_json(quests_file)
    completed_quests = get_data_from_json(finish_file)
    ignore_quests = get_data_from_json(ignore_file)

    finished_tests = [test['test'] for test in completed_quests]
    ignore_tests = [test['tests'][0] for test in ignore_quests]

    # Filters
    quests = [q for q in quests if q['tests'][0] not in finished_tests]  # filter finished
    quests = [q for q in quests if q['tests'][0] not in ignore_tests]  # filter ignored

    for quest in quests:
        print(f"Testing {quest['name']}")
        resault = _get_test_resault(api_key=api_key, filter=quest['filter'])
        if resault[0]:
            dump_to_json(finish_file, _get_finished_quests(api_key))
        else:
            lines = '*' * 100
            space = '\n' * 2
            print(f"{lines}{space}{resault[1]}{space}{lines}{space}{quest['instruction']}{space}{lines}")
            break


if __name__ == '__main__':
    configs = {
        'finish_file': 'finished.json',
        'quests_file': 'quests.json',
        'ignore_file': 'ignore.json',
        'api_key': dotenv_values('.config').get('API_KEY')
    }
    main(**configs)
