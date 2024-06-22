import json
file = open("data.json", "r")
data = json.load(file)["messages"]
file.close()
answer_len = 150
result = "commbined attack on france"
prompt = result.split()[-1]
print(result, end=" ")
while len(result) < answer_len:
    word_after = {}
    for line in data:
        words = line.split()
        for i, word in enumerate(words):
            if word.upper() == prompt.upper() and i < len(words)-1:
                if words[i+1] in word_after.keys():
                    word_after[words[i+1]] += 1
                else:
                    word_after[words[i+1]] = 1
            for j, prev_prompt in enumerate(result.split()):
                if j < len(result.split()) - 5:
                    continue
                if word.upper() == prev_prompt.upper() and i < len(words)-(len(result.split())-j) and words[i+(len(result.split()) - j)] in word_after.keys():
                    word_after[words[i+(len(result.split()) - j)]] += 1
                
    word_after = {key: val for key, val in sorted(word_after.items(), key = lambda ele: ele[1], reverse = True)}
    for word in word_after:
        if word in result:
            continue
        print(word, end=" ")
        result += " " + word
        prompt = word
        break
    else:
        try:
            print(list(word_after.keys())[0], end=" ")
            result += " " + list(word_after.keys())[0]
            prompt = list(word_after.keys())[0]
        except IndexError:
            print("\n#-----No More Data-----#")
            quit()

