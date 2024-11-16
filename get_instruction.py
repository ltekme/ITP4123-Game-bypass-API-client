from _modules import get_data_from_json

quests = get_data_from_json('./data/quests.json')

if __name__ == "__main__":
    for i in quests:
        print('*'*50)
        test_name = i['tests'][0]
        dot_test = test_name.find(".Test")
        print(f"{test_name[16:19]}_{test_name[dot_test+1:dot_test+7]}")
        print(i['instruction'])
        print("\n")