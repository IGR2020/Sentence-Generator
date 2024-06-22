import json
file = open("data.json", "r")
data = json.load(file)["messages"]
file.close()
answer_len = 300
result = "invade germany"
prompt = result.split()[-1]
print(result, end=" ")
while len(result) < answer_len:
    word_after = {}
    for line in data:
        words = line.split()
        for i, word in enumerate(words):
            for wi, prompt in enumerate(result.split()):
                if wi - len(result.split()) < -3:
                    continue
                if word.upper() == prompt.upper() and i < len(words)-(len(result.split())-wi):
                    if words[i+(len(result.split())-wi)] in word_after.keys():
                        word_after[words[i+(len(result.split())-wi)]] += 1*(1/len(result.split())-wi)
                    else:
                        word_after[words[i+(len(result.split())-wi)]] = 1*(1/len(result.split())-wi)
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

