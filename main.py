import json

file = open("data.json")
data = json.load(file)["messages"]
file.close()
answer_len = 100
prompt = "you"
result = prompt

while len(result) < answer_len:
    word_after = {}
    for line in data:
        words = line.split()
        for i, word in enumerate(words):
            if word == prompt and i != len(words)-1:
                if words[i+1] in word_after.keys():
                    word_after[words[i+1]] += 1
                else:
                    word_after[words[i+1]] = 1
    max_value_name = list(word_after.keys())[0]
    second_max_value = max_value_name
    for value in word_after:
        if word_after[value] > word_after[max_value_name]:
            second_max_value = max_value_name
            max_value_name = value
    if max_value_name in result:
        result += " " + second_max_value
        prompt = second_max_value
    else:
        result += " " + max_value_name
        prompt = max_value_name
print(result)
        

