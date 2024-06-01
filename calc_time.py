from _modules import get_data_from_json, dump_to_json
from datetime import datetime, timedelta

task = get_data_from_json('finished.json')
task = sorted(task, key=lambda x: x['time'])

dump_to_json('finished_time_sorted.json', task)

for t in task:
    t['time'] = datetime.strptime(t['time'], '%Y-%m-%dT%H:%M:%S').timestamp()


def epoch_diff(begin_time, end_time):
    return end_time - begin_time


def get_diff_string(diff):
    td = timedelta(seconds=diff)
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds // 60) % 60
    seconds = td.seconds % 60
    time_string = ""
    if days > 0:
        time_string += f"{td.days}d "
    if hours > 0:
        time_string += f"{hours}h "
    if minutes > 0:
        time_string += f"{minutes}m "
    if seconds > 0:
        time_string += f"{seconds}s"
    return time_string or "0s"


number_of_tasks = len(task)
for i in range(number_of_tasks-1):
    if i <= number_of_tasks-1:
        print(task[i]['test'] + " ---> " + task[i+1]['test'])
        print(get_diff_string(epoch_diff(task[i]['time'], task[i+1]['time'])))
        print('*'*50)
    else:
        break
    
time_used = 0
time_used += epoch_diff(task[0]['time'], task[number_of_tasks-1]['time'])
print(f"Total tasks: {number_of_tasks}")
print(f"Total Time Used: {get_diff_string(time_used)}")
