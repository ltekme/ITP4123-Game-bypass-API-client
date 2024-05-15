from _modules import get_data_from_json
import requests

source = 'finished.json'
for task in get_data_from_json(source):
    test_name = task['test']
    dot_test = test_name.find(".Test")
    open(f'logs/{test_name[16:19]}_{test_name[dot_test+1:dot_test+7]}.log', mode='w').write(requests.get(task['logUrl']).content.decode('utf-8'))
