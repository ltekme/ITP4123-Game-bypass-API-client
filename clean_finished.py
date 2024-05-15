from _modules import get_data_from_json, dump_to_json

source = 'finished.json'
output = 'clean_finish.json'

completed_list = []
for quest in get_data_from_json(source):
    completed_list.append(quest['tests'][0])

dump_to_json(output, completed_list)