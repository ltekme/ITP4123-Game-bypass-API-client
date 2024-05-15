from _modules import Quest_Task, dump_to_json, get_data_from_json
'''
Takes in quest api json response file from /api/marks and convert it back to /api/game format

From
{
    "test": "ProjectTestsLib.T01_CredentialTest.Test01_ValidCredential",
    "mark": 10,
    "time": "2024-13-32T26:68:79",
    "logUrl": "<- omitted ->",
    "jsonResultUrl": "<- omitted ->",
    "xmlResultUrl": "<- omitted ->"
}
to
{
    "gameClassOrder": 1,
    "name": "ProjectTestsLib.T01_CredentialTest.Test01_ValidCredential",
    "tests": [
        "ProjectTestsLib.T01_CredentialTest.Test01_ValidCredential"
    ],
    "instruction": "Missing",
    "filter": "test=ProjectTestsLib.T01_CredentialTest.Test01_ValidCredential",
    "timeLimit": 2,
    "reward": 10
    }
}
'''

input = 'finished.json'
output = 'finished_quests.json'

quests = []
for quest in get_data_from_json(input):
    quests.append(
        Quest_Task(
            test = quest['test']
        )
    )

dump_to_json(output, quests)